"""
View logic for handling course messages.
"""

from babel.dates import format_date, format_timedelta
from datetime import datetime

from courseware.courses import get_course_with_access
from django.template.loader import render_to_string
from django.utils.timezone import UTC
from django.utils.translation import get_language, to_locale
from opaque_keys.edx.keys import CourseKey
from web_fragments.fragment import Fragment

from openedx.core.djangoapps.plugin_api.views import EdxFragmentView


class CourseMessageFragmentView(EdxFragmentView):
    """
    A fragment that displays a course message with an alert and call
    to action for three types of users:

    1) Not logged in users are given a link to sign in or register.
    2) Unenrolled users are given a link to enroll.
    3) Enrolled users who get to the page before the course start date
    are given the option to add the start date to their calendar.

    This fragment requires a user_access map as follows:

    user_access = {
        'is_anonymous': True if the user is logged in, False otherwise
        'is_enrolled': True if the user is enrolled in the course, False otherwise
        'is_staff': True if the user is a staff member of the course, False otherwise
    }
    """

    def render_to_fragment(self, request, course_id=None, user_access=None, **kwargs):
        """
        Renders a course message fragment for the specified course.
        """
        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, 'load', course_key)

        # Get time until the start date, if already started, or no start date, value will be zero or negative
        now = datetime.now(UTC())
        delta = course.start - now
        course_start_date = format_date(course.start, locale=to_locale(get_language()))
        already_started = course.start and (course.start - now).days <= 0
        days_until_start_string = "started" if already_started else format_timedelta(delta, locale=to_locale(get_language()))

        # Return None if user is enrolled and course has begun
        if user_access['is_enrolled'] and already_started:
            return None

        # Grab the logo
        image_src = "course_experience/images/xsy_circle.png"

        context = {
            'user_access': user_access,
            'course': course,
            'course_start_date': course_start_date,
            'days_until_start_string': days_until_start_string,
            'already_started': already_started,
            'image_src': image_src,
        }

        html = render_to_string('course_experience/course-message-fragment.html', context)
        return Fragment(html)