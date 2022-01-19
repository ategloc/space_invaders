import urwid

ncounter = 1


def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    if key in ('w', 'W'):
        global ncounter
        ncounter += 1

class QuestionBox(urwid.Filler):
    def keypress(self, size, key):
        global ncounter
        if key != 'enter':
            return super(QuestionBox, self).keypress(size, key)
        self.original_widget = urwid.Text(
            "\n" * ncounter + f"Nice to meet you,\n%s.\n\nPress Q to exit." %
            edit.edit_text)

edit = urwid.Edit(f"What is your name?\n")
fill = QuestionBox(edit)
frame = urwid.Frame(fill, urwid.Edit(f"SpaceInv"))
loop = urwid.MainLoop(frame, unhandled_input=exit_on_q)
loop.run()