#!/usr/bin/env python

import uuid

from boto.mturk.connection import MTurkConnection
from boto.mturk.question import Question, QuestionForm, QuestionContent, ExternalQuestion
from boto.mturk.question import AnswerSpecification, FreeTextAnswer, SelectionAnswer
from boto.mturk.question import Overview
#from boto.mturk.qualification import Qualifications, PercentAssignmentsAbandonedRequirement
#from boto.mturk.qualification import Requirement

from django.contrib.contenttypes.models import ContentType

from pyango_view import str2img

from wt_articles.models import TranslationRequest
from wt_articles.models import SourceArticle, SourceSentence
from wt_articles import MECHANICAL_TURK
from wt_languages.models import TARGET_LANGUAGE
from wt_languages.models import SOURCE_LANGUAGE

from mturk_manager.workflow import task_from_object,load_task_config
from mturk_manager.workflow import TASKCONFIG_DEFAULT
from mturk_manager.models import TaskConfig, TaskAttribute


###########################################
# Functions not required by mturk_manager #
###########################################

def handle_translation_request(trans_req, taskconfig_name=TASKCONFIG_DEFAULT):
    """
    handle_translation_request is an entry point from the management
    command 'translate_mturk'. It takes a Translation Request and breaks
    it into mturk hits representing the request parameters.
    """
    article = trans_req.article
    language = trans_req.target_language
    print 'Translate %s to %s' % (article.title, language)

    # the task config must exist already. not sure how to
    # handle this yet
    task_config = load_task_config(taskconfig_name)

    task_item = task_from_object(trans_req.article)
    task_item.name = 'Translate %s' % article.title
    task_item.config = task_config
    task_item.save()

    # Attach knowledge of target language
    task_attr = TaskAttribute(task_item=task_item,
                              key=TARGET_LANGUAGE,
                              value=language)
    task_attr.save()


def _gen_images(sentences, output_path):
    """
    dunno
    """
    web_path = '/site_media/pydjango_view'
    sentences = []
    width = 350
    extension = 'png'
    for s in urdu_sentences:
        output = '%s/%s.%s' % (output_path, s.id, extension)
        dataurl = '%s/%s.%s' % (web_path, s.id, extension)
        retval = str2img(s.text,
                         #font='Nafees',
                         output=output,
                         width=width)
        data = {
            'type': 'image',
            'subtype': extension,
            'file_path': output,
            'dataurl': dataurl,
            'width': width,
            'text': s.text,
        }
        sentences.append(data)
    return sentences
    
    
#############################
# Required by mturk_manager #
#############################

### PENDING_FUNCTIONS
    
def prepare_media(task_item, retval):
    """
    dunno
    """
    # Gather pertinent info
    source_article = task_item.content_object
    source_sentences = source_article.sourcesentence_set.all()
    print 'weeeee'
    
    img_sentence_info = _gen_images(source_sentences,
                                    '/Users/jd/Projects/playpen/botolearn/pydjango_view')

    return img_sentence_info

def generate_question_form(task_item):
    """
    dunno
    """
    print 'generate_question_form'

def submit_hit(task_item):
    """
    dunno
    """
    print 'submit that hit'

### REVIEW_FUNCTIONS

def update_statuses(task_item):
    """
    dunno
    """
    print 'update_statuses'
    
