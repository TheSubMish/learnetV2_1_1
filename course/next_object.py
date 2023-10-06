from .models import Chapter,Test

def get_next_chapter(course, current_chapter_id):
    chapters = Chapter.objects.filter(course=course).order_by('id')
    
    current_chapter_index = next((
        index for index, 
        chapter in enumerate(chapters) 
        if chapter.id == current_chapter_id
    ), None)
    
    if current_chapter_index is not None and current_chapter_index + 1 < len(chapters):
        return chapters[current_chapter_index + 1]
    
    return None

def get_next_test(course, current_test_id):
    tests = Test.objects.filter(course=course).order_by('id')
    
    current_test_index = next((
        index for index, 
        test in enumerate(tests) 
        if test.id == current_test_id
    ), None)
    
    if current_test_index is not None and current_test_index + 1 < len(tests):
        return tests[current_test_index + 1]
    
    return None