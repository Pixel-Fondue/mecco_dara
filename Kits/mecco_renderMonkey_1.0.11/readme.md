#RenderMonkey
**Rendering utilities for MODO**

RM has several inter-related featuresets: easy progressive rendering, render range, combine pass groups, and batch rendering.

We wrote RM because we wanted to use it in our own work, and thought other people might want to use it too.

- **Simple progressive rendering** - maximum quality with minimum effort

- **Render range** - e.g. "1-5, 10, 20-15" renders frames [1,2,3,4,5,10,20,19,18,17,16,15]


- **Combine pass groups** - e.g. a scene with one pass group called 'shots' and another called 'colorways', render each shot for each colorway


- **Batch rendering** - Line 'em up and knock 'em down: set up all of your render jobs from all of your scene files and let The Monkey do the rest.

##To Do
- Combine Pass Groups only works with group's channels, not items (if present). Fix.
- Add "quick batch" command
- Add "new batch" command
- Add "open batch" command
- Add "add task" command (w/multi-select)
- Add "edit task" command (by index)
- Add tree view