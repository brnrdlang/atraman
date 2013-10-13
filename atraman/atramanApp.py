from datetime import datetime, date
from calendar import Calendar
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, ListProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
import os

pwd = os.path.dirname(__file__)

class DateButton(Button):
    def __init__(self, date, callback, **kwargs):
        super(DateButton, self).__init__(**kwargs)
        self.date = date
        self.bind(on_press = callback)

#Builder.load_file(os.path.join(pwd, 'calendar.kv'))

class CalendarWidget(BoxLayout):
    
    month = StringProperty('')
    year = StringProperty('')
    calendar_layout = ObjectProperty(None)
    calendar_btns = ListProperty([])
    calendar = ObjectProperty(Calendar())

    def __init__(self, **kwargs):
        super(CalendarWidget, self).__init__(**kwargs)

        self.date = date.today()
        self.month = self.date.strftime('%B')
        self.year = str(self.date.year)

    def on_calendar_layout(self, instnce, value):
        self.create_calendar()

    def create_calendar(self):
        self.calendar_layout.clear_widgets()
        def do_day_clicked(instance):
            pass

        for week in self.calendar.monthdatescalendar(self.date.year, self.date.month):
            self.calendar_btns.extend([DateButton(date, do_day_clicked,text=str(date.day), name=str(date))
                             for date in week])

        for btn in self.calendar_btns:
            self.calendar_layout.add_widget(btn)

    def do_month_before(self):
        self.date = date(self.date.year, self.date.month - 1, 1)

    def do_month_next(self):
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
