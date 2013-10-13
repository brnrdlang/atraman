from datetime import datetime, date
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class CalendarWidget(BoxLayout):
    
    month = StringProperty('')
    year = StringProperty('')

    def __init__(self, **kwargs):
        super(CalendarWidget, self).__init__(**kwargs)
        self.date = date.today()
        self.month = self.date.strftime('%B')
        self.year = str(self.date.year)

    def do_month_before(self):
        self.date = date(self.date.year, self.date.month - 1, 1)
        

    def do_month_next(self):
        pass

    def do_day_clicked(self, day):
        pass

#will be used later when there is more than the calendar
class MenuScreen(Screen):
    pass

class CalendarScreen(Screen):
    pass

sm = ScreenManager()

class AtramanApp(App):

    def build(self):
        sm.switch_to(CalendarScreen(name='calendar'))
        return sm

if __name__ == '__main__':
    AtramanApp().run()
