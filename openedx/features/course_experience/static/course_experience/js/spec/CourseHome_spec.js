/* globals Logger, loadFixtures */

import { CourseHome } from '../CourseHome';

describe('Course Home factory', () => {
  describe('Ensure course tool click logging', () => {
    beforeEach(() => {
      loadFixtures('course_experience/fixtures/course-home-fragment.html');
      const home = new CourseHome({
        courseToolLink: '.course-tool-link',
      });
      spyOn(Logger, 'log');
    });

    it('sends an event when an course tool is clicked', () => {
      document.querySelector('.course-tool-link').dispatchEvent(new Event('click'));
      const courseToolName = document.querySelector('.course-tool-link').text.trim().toLowerCase();
      expect(Logger.log).toHaveBeenCalledWith(
        'edx.course.home.course_tool.accessed',
        {
          tool_name: courseToolName,
        },
      );
    });
  });
});
