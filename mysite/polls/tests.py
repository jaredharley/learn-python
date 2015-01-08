import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from polls.models import Question

## Functions

def create_question(question_text, offset):
    """
    Creates a question with the provided question text and sets the
    published date to the number of days offset for now (positive for
    future, negative for past).
    """
    time = timezone.now() + datetime.timedelta(days=offset)
    return Question.objects.create(question_text=question_text, pub_date=time)

## Classes

class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions
        where the publish date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions
        where the publish date is older than one day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions
        where the publish date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        question = Question(pub_date=time)
        self.assertEqual(question.was_published_recently(), True)

class QuestionViewTests(TestCase):
    """
    Contains test cases for the question view.
    """
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_index_view_with_a_past_question(self):
        """
        Questions with a publish date in the past should be displayed
        on the index page.
        """
        create_question(question_text="Past question.", offset=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
        
    def test_index_view_with_a_future_question(self):
        """
        Questions with a publish date in the future should not be 
        displayed on the index page.
        """
        create_question(question_text="Future question.", offset=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text="Past question.", offset=-30)
        create_question(question_text="Future question.", offset=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", offset=-30)
        create_question(question_text="Past question 2.", offset=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
        
class QuestionIndexDetailTests(TestCase):
    """
    Contains test cases for the details view
    """
    
    def test_detail_view_with_a_future_question(self):
        """
        The question detail view should return a 404 for
        any question with a future publish date.
        """
        future_question = create_question(question_text='Future question.', offset=5)
        response = self.client.get(reverse('polls:detail',
                                   args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)
    
    def test_detail_view_with_a_past_question(self):
        """
        The question detail view should display a question
        when the publish date is in the past.
        """
        past_question = create_question('Past Question.', -5)
        response = self.client.get(reverse('polls:detail',
                                   args=(past_question.id,)))
        self.assertContains(response, past_question.question_text,
                                      status_code=200)