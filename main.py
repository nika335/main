from kivy.app import App
from kivy.lang import Builder
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen, SwapTransition
import re
import sqlite3


class MenuScreen(Screen):
    pass


class Adding(Screen):
    pass

class Subt(Screen):
    pass

class FloatInput(TextInput):
    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join(
                re.sub(pat, '', s)
                for s in substring.split('.', 1)
            )
        return super().insert_text(s, from_undo=from_undo)

class Main(App):

    def build(self):
        sm = ScreenManager(transition=SwapTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(Adding(name='adding'))
        sm.add_widget(Subt(name='sub'))
        con = sqlite3.connect('ss.db')
        c = con.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS first (name INTEGER, ws INTEGER)')
        c.execute('INSERT INTO first VALUES (?, ?)', (0, 10))
        con.commit()
        con.close()

        return sm

    def mainn(self):
            try:
                con = sqlite3.connect('ss.db')
                c = con.cursor()
                c.execute('SELECT ws FROM first')
                records = c.fetchall()
                con.close()
                return str(records[0][0])
            except sqlite3.OperationalError:
                return "10"

    def add(self):
        try:
            adding_screen = self.root.get_screen('adding')
            input_value = int(adding_screen.ids.inp.text)
            con = sqlite3.connect('ss.db')
            c = con.cursor()
            c.execute(f'INSERT INTO first VALUES (?, ?)', (input_value, 10))
                    
            adding_screen.ids.inp.text = ''
            con.commit()
            con.close()
        except ValueError:
            pass

    def subtract(self):
        try:
            adding_screen = self.root.get_screen('sub')
            input_value = int(adding_screen.ids.inp.text)
            con = sqlite3.connect('ss.db')
            c = con.cursor()
            c.execute(f'INSERT INTO first VALUES (?, ?)', (-input_value, 10))    
            adding_screen.ids.inp.text = ''
            con.commit()
            con.close()
        except ValueError:
            pass

    def show(self):
        menu = self.root.get_screen('menu')
        con  = sqlite3.connect('ss.db')
        c = con.cursor()
        c.execute('SELECT SUM(name) FROM first')
        records = c.fetchall()
        x = records[0][0]
        fin = x/1000
        menu.ids.show.text = str(round(fin, 2))
        con.commit()
        con.close()

if __name__ == '__main__':
    Main().run()