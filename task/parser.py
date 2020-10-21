from model.training_model import TrainingSession, TrainingWeek, TrainingDay


class Parser:

    def __init__(self, driver, week_start, activity_type):
        self.activity_type = activity_type
        self.week_start = week_start
        self.driver = driver

    def parse(self, weeks_forward):
        driver = self.driver

        weeks = []
        for week_num in range(0, weeks_forward):
            weeks.append(self._parse_week(driver, week_num))
            agenda = driver.find_element_by_id("agenda")
            agenda_elems = agenda.find_elements_by_tag_name("a")
            for agenda_elem in agenda_elems:
                if agenda_elem.text is not None and agenda_elem.text == "volgende":
                    agenda_elem.click()

        return weeks

    def _parse_week(self, driver, week_num, day_event_class="internal-event-day-"):
        print(f"parsing week #{week_num + 1}")
        schedule_content_elem = driver.find_element_by_id("schedule_content")
        all_days_schedule = schedule_content_elem.find_elements_by_class_name("cal_column")

        days = []
        for day_schedule in all_days_schedule:
            session_elems = day_schedule.find_elements_by_tag_name("div")
            training_day = TrainingDay()
            for session_elem in session_elems:
                div_class = session_elem.get_attribute("class")
                if day_event_class in div_class:
                    time_elem = session_elem.find_element_by_class_name("time")
                    time_text = time_elem.text
                    session_id = session_elem.get_attribute("id")
                    class_name = session_elem.find_element_by_class_name("classname").text
                    training_session = TrainingSession(time_text, session_id, class_name)
                    training_day.sessions.append(training_session)
                    if training_day.day is None:
                        day_str = div_class[div_class.find(day_event_class) + len(day_event_class):]
                        training_day.set_day(day_str)

            days.append(training_day)

        training_week = TrainingWeek(activity_type=self.activity_type.name, week_start=days[0].day, days=days)

        return training_week
