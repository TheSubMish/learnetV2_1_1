from .models import Course

def course_validate(error_msg_dict):
    error = {
        'courseTitle': '',
        'courseDescrip': '',
        'category': '',
        'courseImage': ''
    }

    try:
        if error_msg_dict['category']:
            error['category'] = "Select Category Of Your Course"
            return error
    except KeyError:
        pass
    
    try:
        if error_msg_dict['courseTitle']:
            error['courseTitle'] = "Course With This Name Already Exists"
            return error
    except KeyError:
        pass

    error_msg = error_msg_dict['__all__'][0]['message']
    
    if 'Name' in error_msg:
        error['courseTitle'] = error_msg
    if 'Description' in error_msg:
        error['courseDescrip'] = error_msg
    if 'category' in error_msg:
        error['category'] = error_msg
    if 'Image' in error_msg:
        error['courseImage'] = error_msg
    return error

def chapter_validate(error_msg_dict):
    error = {
        'course': '',
        'chapterName': '',
        'chapterBody': ''
    }
    error_msg = error_msg_dict['__all__'][0]['message']
    if 'Course' in error_msg:
        error['course'] = error_msg
    if 'Name' in error_msg:
        error['chapterName'] = error_msg
    if 'Content' in error_msg:
        error['chapterBody'] = error_msg
    return error

def test_validate(error_msg_dict):
    error = {
        'course': '',
        'title': '',
        'question': '',
        'option1': '',
        'option2': '',
        'option3': '',
        'option4': '',
        'corAns': ''
    }

    error_msg = error_msg_dict['__all__'][0]['message']
    if 'Course' in error_msg:
        error['course'] = error_msg
    if 'Title' in error_msg:
        error['title'] = error_msg
    if 'Question' in error_msg:
        error['question'] = error_msg
    if 'One' in error_msg:
        error['option1'] = error_msg
    if 'Two' in error_msg:
        error['option2'] = error_msg
    if 'Three' in error_msg:
        error['option3'] = error_msg
    if 'Four' in error_msg:
        error['option4'] = error_msg
    if 'Answer' in error_msg:
        error['corAns'] = error_msg
    return error