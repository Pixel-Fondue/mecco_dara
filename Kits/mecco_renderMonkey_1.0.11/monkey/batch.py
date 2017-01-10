# python

import lx, modo
import os, traceback, sys, re, time
import util, defaults, io, render, passes, yaml

from symbols import *

_STATUS = []
_ABORT = False

def batch_status_file(batch_file_path):
    split = os.path.splitext(batch_file_path)
    return "%s_%s%s" % (split[0], STATUS_FILE_SUFFIX, split[1])


def batch_dryRun_file(batch_file_path):
    split = os.path.splitext(batch_file_path)
    return "%s_%s%s" % (split[0], DRYRUN_FILE_SUFFIX, '.txt')


def batch_status_create(data, batch_file_path):
    if not os.path.isfile(batch_status_file(batch_file_path)):
        status_file = open(batch_status_file(batch_file_path), 'w')
        status_file.write(io.yamlize(data))
        status_file.close()


def batch_dryRun_write(data, batch_file_path):
    status_file = open(batch_dryRun_file(batch_file_path), 'w')
    status_file.write("{}\n\n".format(time.asctime( time.localtime(time.time()) )) + "\n".join([i for i in data]))
    status_file.close()


def batch_dryRun_reset(batch_file_path):
    if not os.path.isfile(batch_dryRun_file(batch_file_path)):
        status_file = open(batch_dryRun_file(batch_file_path), 'w')
        status_file.write('')
        status_file.close()


def batch_has_status(batch_file_path):
    if os.path.isfile(batch_status_file(batch_file_path)):
        return True

    return False


def batch_status_reset(batch_file_path):
    status_file = open(batch_status_file(batch_file_path), 'w')
    data = io.read_yaml(batch_file_path)

    try:
        status_file.write(yaml.dump(data, indent=4, width=999, default_flow_style=False).replace("\n-", "\n\n-"))
    except:
        util.debug(traceback.format_exc())
        status_file.close()
        return False

    status_file.close()
    return True


def batch_status_delete(batch_file_path):
    return os.remove(batch_status_file(batch_file_path))


def set_task_status(batch_file_path, task_index, status):
    batch_file_path = batch_status_file(batch_file_path)
    batch = io.read_yaml(batch_file_path)

    if not batch:
        return False

    try:
        if STATUS not in batch[task_index] or not isinstance(batch[task_index][STATUS], list):
            batch[task_index][STATUS] = []

        batch[task_index][STATUS] = [i for i in batch[task_index][STATUS] if not i.startswith(TASK)]
        batch[task_index][STATUS].append("%s %s" % (TASK, status))

        io.write_yaml(batch, batch_file_path)
        return True
    except:
        status("Problem writing task status to batch file.")
        return False


def get_task_status(batch_file_path, task_index):
    batch_file_path = batch_status_file(batch_file_path)
    batch = io.read_yaml(batch_file_path)

    if not batch:
        return STATUS_AVAILABLE

    if STATUS in batch[task_index]:
        for i in batch[task_index][STATUS]:
            if i.startswith(TASK) and STATUS_AVAILABLE not in i:
                return i

    return STATUS_AVAILABLE


def set_frame_status(batch_file_path, task_index, frame_number, status):
    batch_file_path = batch_status_file(batch_file_path)
    batch = io.read_yaml(batch_file_path)

    if not batch:
        return False

    try:
        if STATUS not in batch[task_index] or not isinstance(batch[task_index][STATUS], list):
            batch[task_index][STATUS] = []

        batch[task_index][STATUS] = [
            i for i in batch[task_index][STATUS] if not int(re.search('^[0-9]*', i).group(0)) == frame_number
            ]

        batch[task_index][STATUS].append("%04d %s" % (frame_number, status))

        io.write_yaml(batch, batch_file_path)
        return True
    except:
        status("Problem writing frame status to batch file.")
        return False


def get_frame_status(batch_file_path, task_index, frame_number):
    batch_file_path = batch_status_file(batch_file_path)
    batch = io.read_yaml(batch_file_path)

    if not batch:
        return STATUS_AVAILABLE

    if STATUS in batch[task_index]:
        for i in batch[task_index][STATUS]:
            if int(re.search('^[0-9]*', i).group(0)) == frame_number and STATUS_AVAILABLE not in i:
                return i

    return STATUS_AVAILABLE


def status(message):
    global _STATUS
    util.status(message)
    _STATUS.append(message)

def status_reset():
    global _STATUS
    _STATUS = []


def run(batch_file_path, dry_run=False, res_multiply=1):

    global _ABORT

    restore = {}
    status_reset()

    util.debug('Setting up job.')
    render.to_console(True)

    restore['autoThreads'] = lx.eval('pref.value render.autoThreads ?')
    lx.eval('pref.value render.autoThreads true')

    batch = io.read_yaml(batch_file_path)

    if not batch:
        status("Unable to read YAML.")
        return lx.symbol.e_FAILED

    if batch_has_status(batch_file_path):
        reset = modo.dialogs.yesNoCancel(
            'Reset Batch',
            "Batch file in progress. Reset and start over?\n\nYes: Reset\nNo: Continue\nCancel: Abort"
        )
        if reset in ('ok', 'yes'):
            status("\n\n********\n\n")
            status("Resetting batch file.")
            if not batch_status_reset(batch_file_path):
                status("Could not reset status file. Abort.")
                sys.exit()
        elif reset == "cancel":
            status("User cancel.")
            sys.exit()
        else:
            status("Continue batch as-is.")
    else:
        batch_status_create(batch, batch_file_path)

    # std_dialog = lx.service.StdDialog()
    # main_monitor = lx.object.Monitor(std_dialog.MonitorAllocate('Running Batch'))
    # main_monitor.Initialize(len(batch))

    util.debug("Scanning for task.")
    for task_index, task in enumerate(batch):

        if not get_task_status(batch_file_path, task_index) == STATUS_AVAILABLE:
            status("ERROR: Task %s status: '%s'. Skip task." % (task_index, get_task_status(batch_file_path, task_index)))
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            continue

        if SCENE_PATH not in task:
            status("ERROR: No path specified for task %s. Skip task." % task_index)
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            continue

        task_path = util.expand_path(task[SCENE_PATH])

        if not os.path.isfile(task_path):
            status('ERROR: "%s" not found. Skip task.' % os.path.basename(task_path))
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            continue

        #
        # Open Scene
        #

        status("\n\n********\n\n")
        status("Begin task %s (%s)" % (task_index, os.path.basename(task_path)))

        try:
            lx.eval('scene.open {%s} normal' % task_path)
            scene = modo.Scene()
            status('Opened Scene: ' + task_path)

        except:
            status('ERROR: Failed to open "%s". Skip task.' % os.path.basename(task_path))
            util.debug(traceback.format_exc())
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            continue

        #
        # Parse Frames
        #

        frames = task[FRAMES] if FRAMES in task else util.get_scene_render_range()
        if not frames:
            frames = defaults.get(FRAMES)

        try:
            frames_list = util.frames_from_string(frames)

            if not isinstance(frames_list, list) or len(frames_list) < 1:
                status('ERROR: "%s" contains no valid frames. Skip task.') % frames
                set_task_status(batch_file_path, task_index, STATUS_FAILED)
                lx.eval('!scene.close')
                continue

        except:
            status('ERROR: Failed to parse frame range "{}". Skip task.'.format(frames))
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        if not frames_list:
            status("ERROR: No valid frames to render. Skip task.")
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        if not [i for i in frames_list if get_frame_status(batch_file_path, task_index, i) == STATUS_AVAILABLE]:
            status("ERROR: No available frames. Skip task.")
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        status(FRAMES + ": " + ", ".join([str(i) for i in frames_list]))


        #
        # Parse Output Pattern
        #

        try:
            scene_pattern = scene.renderItem.channel(lx.symbol.sICHAN_POLYRENDER_OUTPAT).get()
            output_pattern = task[PATTERN] if PATTERN in task else scene_pattern
        except:
            status('ERROR: Failed to parse suffix (i.e. output pattern). Skip task.')
            util.debug(traceback.format_exc())
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        status(PATTERN + ": " + output_pattern)

        #
        # Parse scene width/height
        #

        try:
            scene_width = float(scene.renderItem.channel(lx.symbol.sICHAN_POLYRENDER_RESX).get())
            scene_height = float(scene.renderItem.channel(lx.symbol.sICHAN_POLYRENDER_RESY).get())

            if WIDTH in task:
                x = round(float(task[WIDTH]))
                width = x if x > 0 else None
            else:
                width = 0

            if HEIGHT in task:
                y = round(float(task[HEIGHT]))
                height = y if y > 0 else None
            else:
                height = 0

            if not width and not height:
                width = scene_width
                height = scene_height

            elif width and not height:
                height = int(round(width * (scene_height/scene_width)))

            elif height and not width:
                width = int(round(height * (scene_width/scene_height)))

            width *= res_multiply
            height *= res_multiply

        except:
            status('ERROR: Something went wrong with width/height. Skip task.')
            util.debug(traceback.format_exc())
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        status("{}: {}; {}: {}".format(WIDTH, width, HEIGHT, height))

        #
        # Parse outputs
        #

        try:
            outputs = task[OUTPUTS] if OUTPUTS in task else None
            if isinstance(outputs, str):
                outputs = [outputs]

            output_items = set()
            if outputs:
                for i in outputs:
                    if scene.item(i) and scene.item(i).type == lx.symbol.sITYPE_RENDEROUTPUT:
                        output_items.add(scene.item(i))
                    else:
                        status("CAUTION: '%s' is not a valid render output. Ignore." % i)

        except:
            status('ERROR: Something went wrong getting render outputs. Skip task.')
            util.debug(traceback.format_exc())
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        if output_items:
            status(OUTPUTS + ": " + "; ".join([i.name for i in output_items]))

        #
        # Parse camera
        #

        try:
            camera = task[CAMERA] if CAMERA in task else None

            if camera and scene.item(camera).type != lx.symbol.sITYPE_CAMERA:
                status('ERROR: Could not set render camera. Skip task.')
                continue

        except:
            status('ERROR: Something went wrong setting the render camera. Skip task.')
            util.debug(traceback.format_exc())
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        if camera:
            status(CAMERA + ": " + camera)

        #
        # Parse pass group
        #

        master_pass_group = None
        pass_group_names = task[GROUPS] if GROUPS in task else None
        try:
            if pass_group_names:
                pass_group_names = pass_group_names if isinstance(pass_group_names, list) else [pass_group_names]

                pass_groups = set()
                for group in pass_group_names:
                    i = scene.item(group)
                    if i:
                        pass_groups.add(i)
                    else:
                        status('CAUTION: Could not find group called "%s". Ignore.' % group)

                if len(pass_groups) > 1:
                    master_pass_group = passes.create_master_pass_group(list(pass_groups))
                    master_pass_group = master_pass_group if master_pass_group else None
                elif len(pass_groups) == 1:
                    master_pass_group = list(pass_groups)[0]
                else:
                    master_pass_group = None

        except:
            status('ERROR: Failed to parse pass groups "{}". Skip task.'.format(pass_group_names))
            util.debug(traceback.format_exc())
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        if master_pass_group:
            status(GROUPS + ": " + master_pass_group.name)

        #
        # Parse render destination
        #

        try:
            destination = task[DESTINATION] if DESTINATION in task else defaults.get(DESTINATION)

            if destination == '*':
                destination_dirname = None
            else:
                destination = util.expand_path(destination)

                if os.path.splitext(destination)[1]:
                    destination_filename = os.path.splitext(os.path.basename(destination))[0]
                    destination_dirname = os.path.dirname(destination)
                else:
                    destination_filename = os.path.splitext(os.path.basename(task_path))[0]
                    destination_dirname = destination

                destination = os.path.sep.join([destination_dirname, destination_filename])

        except:
            status('ERROR: Failed to establish valid destination. Skip task.')
            util.debug(traceback.format_exc())
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        if destination_dirname and not io.test_writeable(destination_dirname):
            status("ERROR: Could not write to destination. Skip task.")
            util.debug(traceback.format_exc())
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        status(DESTINATION + ": " + str(destination))


        #
        # Parse Image Saver
        #

        try:
            if FORMAT in task:
                imagesaver = task[FORMAT]
            else:
                imagesaver = defaults.get(FORMAT)

            if (DESTINATION in task and task[DESTINATION] == '*') or (FORMAT in task and task[FORMAT] == '*'):
                imagesaver = None

            if imagesaver and not util.get_imagesaver(imagesaver):
                status("ERROR: '%s' is not a valid image saver. Skip task." % imagesaver)
                set_task_status(batch_file_path, task_index, STATUS_FAILED)
                lx.eval('!scene.close')
                continue

        except:
            status('ERROR: Failed to get image saver. Skip task.')
            util.debug(traceback.format_exc())
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        status(FORMAT + ": " + str(imagesaver))


        #
        # Set render channels
        #

        render_channels = task[RENDER_CHANNELS] if RENDER_CHANNELS in task else {}
        if render_channels:
            try:
                for channel,  value in render_channels.iteritems():
                    try:
                        scene.renderItem.channel(channel).set(value)
                        status('{}: {} = {}'.format(
                            RENDER_CHANNELS,
                            scene.renderItem.channel(channel).name,
                            scene.renderItem.channel(channel).get()
                        ))
                    except:
                        status("ERROR: %s could not be set. Skip task.")
                        util.debug(traceback.format_exc())
                        lx.eval('!scene.close')
                        continue
            except:
                status("ERROR: Failed to set render channels. Skip task.")
                util.debug(traceback.format_exc())
                set_task_status(batch_file_path, task_index, STATUS_FAILED)
                lx.eval('!scene.close')
                continue

        try:
            scene.renderItem.channel(lx.symbol.sICHAN_POLYRENDER_OUTPAT).set(output_pattern)
            scene.renderItem.channel(lx.symbol.sICHAN_POLYRENDER_RESX).set(width)
            scene.renderItem.channel(lx.symbol.sICHAN_POLYRENDER_RESY).set(height)

        except:
            status("ERROR: Failed to set render channels. Skip task.")
            util.debug(traceback.format_exc())
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        #
        # Set render camera
        #

        if camera:
            try:
                lx.eval('render.camera {%s}' % camera)
            except:
                status("ERROR: Failed to set render camera. Skip task.")
                util.debug(traceback.format_exc())
                set_task_status(batch_file_path, task_index, STATUS_FAILED)
                lx.eval('!scene.close')
                continue

        #
        # Set output items
        #

        try:
            if output_items:

                # since outputs were explicitly chosen by user, we need to override
                # the default behavior of including alphas in output files, and instead
                # output all render outputs manually. This means assigning the destination
                # to the output's filename and then rendering to * in the render command.

                # But, if destination is * already, we'll assume the user knows what they're
                # doing and honor that.

                force_dest = True if destination and destination != '*' else False

                for o in scene.items(lx.symbol.sITYPE_RENDEROUTPUT):
                    o.channel(lx.symbol.sICHAN_TEXTURELAYER_ENABLE).set(0)
                for o in output_items:
                    o.channel(lx.symbol.sICHAN_TEXTURELAYER_ENABLE).set(1)

                    if force_dest:
                        if not o.channel(lx.symbol.sICHAN_RENDEROUTPUT_FILENAME).get():
                            o.channel(lx.symbol.sICHAN_RENDEROUTPUT_FILENAME).set(destination)
                        if not o.channel(lx.symbol.sICHAN_RENDEROUTPUT_FORMAT).get():
                            o.channel(lx.symbol.sICHAN_RENDEROUTPUT_FORMAT).set(imagesaver if imagesaver else defaults.get(FORMAT))

                if force_dest:
                    destination = '*'
                    imagesaver = None
        except:
            status("ERROR: Failed to set output visibility. Skip task.")
            util.debug(traceback.format_exc())
            set_task_status(batch_file_path, task_index, STATUS_FAILED)
            lx.eval('!scene.close')
            continue

        #
        # Set pass group
        #

        try:
            if master_pass_group:
                master_pass_group_name = master_pass_group.name
            else:
                master_pass_group_name = None
        except:
            status("CAUTION: Failed to set master pass group name. Ignore.")
            util.debug(traceback.format_exc())
            master_pass_group_name = None


        #
        # Run task commands
        #

        failed = False
        if COMMANDS in task:
            for command in task[COMMANDS]:
                try:
                    lx.eval(command)
                except:
                    status('ERROR: Command "{}" failed. Skip frame.'.format(command))
                    util.debug(traceback.format_exc())
                    failed = True
        if failed:
            continue


        #
        # Render Frames
        #

        for frame in frames_list:
            # try:
            #     main_monitor.Increment(1/len(frames_list))
            # except:
            #     status("User abort")
            #     break

            #
            # Set render frame
            #

            try:
                scene.renderItem.channel('first').set(frame)
                scene.renderItem.channel('last').set(frame)
            except:
                status("ERROR: Failed to set first/last frames to %04d. Skip frame." % frame)
                util.debug(traceback.format_exc())
                continue

            #
            # Check frame status
            #

            if not get_frame_status(batch_file_path, task_index, frame) == STATUS_AVAILABLE:
                status("FRAME BUSY: %s. Skip frame." % get_frame_status(batch_file_path, task_index, frame))
                continue

            set_frame_status(batch_file_path, task_index, frame, STATUS_IN_PROGRESS)
            status("\n- Rendering frame %04d." % frame)


            #
            # Run task commands
            #

            failed = False
            if FRAME_COMMANDS in task:
                for command in task[FRAME_COMMANDS]:
                    try:
                        lx.eval(command)
                    except:
                        status('ERROR: Command "{}" failed. Skip frame.'.format(command))
                        util.debug(traceback.format_exc())
                        failed = True
            if failed:
                continue


            #
            # Build render command
            #

            if RENDER_OVERRIDE in task:
                render_command = task[RENDER_OVERRIDE]
            else:
                args = util.build_arg_string({
                        "filename": destination,
                        "format": imagesaver,
                        "group": master_pass_group_name
                    })

                render_command = 'render.animation' + args

            #
            # Render the frame
            #

            try:
                if dry_run:
                    status("Render Command: " + render_command)
                    status("(assumed success)")
                else:
                    try:
                        lx.eval(render_command)
                    except:
                        status("USER ABORT")
                        set_frame_status(batch_file_path, task_index, frame, STATUS_ABORT)
                        set_task_status(batch_file_path, task_index, STATUS_ABORT)
                        lx.eval('!scene.close')
                        lx.eval('file.open {{{}}}'.format(batch_status_file(batch_file_path)))
                        _ABORT = True
                        break
                set_frame_status(batch_file_path, task_index, frame, STATUS_COMPLETE)
            except:
                status('ERROR: "%s" failed. Skip frame.' % render_command)
                util.debug(traceback.format_exc())

        if _ABORT:
            util.status('User aborted task %s (%s). Stop.' % (task_index, os.path.basename(task_path)))
            break

        #
        # Task complete
        #

        util.status('Completed task %s (%s). Continue.' % (task_index, os.path.basename(task_path)))
        set_task_status(batch_file_path, task_index, STATUS_COMPLETE)
        lx.eval('!scene.close')

    #
    # Clean up
    #

    render.to_console(False)
    lx.eval('pref.value render.autoThreads %s' % restore['autoThreads'])

    if dry_run:
        batch_dryRun_write(_STATUS, batch_file_path)
        lx.eval('file.open {%s}' % batch_dryRun_file(batch_file_path))
    else:
        lx.eval('file.open {{{}}}'.format(batch_status_file(batch_file_path)))

    return lx.symbol.e_OK
