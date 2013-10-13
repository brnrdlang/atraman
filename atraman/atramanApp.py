from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class CalendarScreen(Screen):
    pass

#will be used later when there is more than the calendar
class MenuScreen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(CalendarScreen(name='calendar'))

class AtramanApp():

    def build(self):
        return sm

if __name__ == '__main__':
    AtramanApp().run()
