from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
import json

from .models import Course, Chapter, Test
from .forms import CourseForm, ChapterForm, TestForm
from .validations import course_validate, chapter_validate, test_validate
from teacher.models import Teacher
from .next_object import get_next_chapter,get_next_test

# Create your views here.
class AddCourse(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = 'addCourse.html'
    model = Course
    form_class = CourseForm

    def dispatch(self, request, *args, **kwargs):
        try:
            Teacher.objects.get(user=request.user)
        except:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        error_msg_dict = json.loads(form.errors.as_json())
        error = course_validate(error_msg_dict)
        return render(self.request, self.template_name, {'form': form, 'error': error})
    
    def form_valid(self, form):
        teacher = Teacher.objects.get(user=self.request.user)
        form.instance.teacher = teacher
        course_title = form.cleaned_data['courseTitle']
        
        if Course.objects.filter(courseTitle=course_title).exists():
            form.add_error('courseTitle', 'Course With This Name Already Exists')
            return self.form_invalid(form)
        
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        form = self.request.POST
        return reverse('addchapter', kwargs={'slug': slugify(form.get('courseTitle'))})


class AddChapter(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    template_name = 'addChapter.html'
    model = Chapter
    form_class = ChapterForm

    def dispatch(self, request, *args, **kwargs):
        try:
            Teacher.objects.get(user=request.user)
        except:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = Teacher.objects.get(user=self.request.user)
        courses = Course.objects.filter(teacher=user)
        kwargs['teacher_courses'] = courses
        return kwargs
    
    def get_initial(self):
        initial = super(AddChapter, self).get_initial()
        initial['course'] = Course.objects.get(slug=self.kwargs['slug'])
        return initial

    def form_invalid(self, form):
        error_msg_dict = json.loads(form.errors.as_json())
        error = chapter_validate(error_msg_dict)
        return render(self.request, self.template_name, {'form': form, 'error': error})
    
    def get_success_url(self):
        form = self.request.POST
        course = Course.objects.get(slug=self.kwargs['slug'])
        # next takes to add test
        if form.get('next'):
            return reverse_lazy('addtest', kwargs={'slug': course.slug})
        # add_more takes to add another chapter
        if form.get('add_more'):
            return reverse('addchapter', kwargs={'slug': course.slug})


class AddTest(AddChapter):
    login_url = '/login/'
    template_name = 'addTest.html'
    model = Test
    form_class = TestForm

    def dispatch(self, request, *args, **kwargs):
        try:
            Teacher.objects.get(user=request.user)
        except:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_initial(self):
        initial = super(AddChapter, self).get_initial()
        initial['course'] = Course.objects.get(slug=self.kwargs['slug'])
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = Teacher.objects.get(user=self.request.user)
        courses = Course.objects.filter(teacher=user)
        kwargs['teacher_courses'] = courses
        return kwargs
    
    def form_invalid(self, form):
        error_msg_dict = json.loads(form.errors.as_json())
        error = test_validate(error_msg_dict)
        return render(self.request, self.template_name, {'form': form, 'error': error})
    
    def get_success_url(self):
        form = self.request.POST
        course = Course.objects.get(slug=self.kwargs['slug'])
        # next takes to add test
        if form.get('publish'):
            course.published = True
            course.save()
            return '/teacher/dashboard/'
        # add_more takes to add another chapter
        if form.get('add_more'):
            return reverse('addtest', kwargs={'slug': course.slug})


class UpdateCourse(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    template_name = 'updateCourse.html'
    model = Course
    form_class = CourseForm

    def get_success_url(self):
        course = self.model.objects.get(slug=self.object.slug)
        slug = course.slug
        try:
            pk = Chapter.objects.filter(course=course).first().pk
        except AttributeError:
            return reverse_lazy('addchapter', kwargs={'slug': slug})
        return reverse_lazy('updatechapter', kwargs={'slug': slug, 'pk': pk})

    def dispatch(self, request, *args, **kwargs):
        try:
            Teacher.objects.get(user=request.user)
        except:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        error_msg_dict = json.loads(form.errors.as_json())
        error = course_validate(error_msg_dict)
        return render(self.request, self.template_name, {'form': form, 'error': error})


class UpdateChapter(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    template_name = 'updateChapter.html'
    model = Chapter
    form_class = ChapterForm

    def dispatch(self, request, *args, **kwargs):
        try:
            Teacher.objects.get(user=request.user)
        except:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = Teacher.objects.get(user=self.request.user)
        courses = Course.objects.filter(teacher=user)
        kwargs['teacher_courses'] = courses
        return kwargs
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['slug'])
        context['chapter'] = Chapter.objects.get(id=self.kwargs['pk'])
        return context

    def form_invalid(self, form):
        error_msg_dict = json.loads(form.errors.as_json())
        error = chapter_validate(error_msg_dict)
        return render(self.request, self.template_name, {'form': form, 'error': error})
    
    def get_success_url(self):
        form = self.request.POST
        course = Course.objects.get(slug=self.kwargs['slug'])
        # next takes to another chapter
        if form.get('next'):
            next_chapter = get_next_chapter(course,self.kwargs['pk'])
            if not next_chapter:
                return reverse('addchapter', kwargs={'slug': course.slug})
            else:
                return reverse('updatechapter', kwargs={'slug': course.slug, 'pk': next_chapter.pk})
        # add_more takes to update test or add test
        if form.get('add_more'):
            try:
                pk = Test.objects.filter(course=course).first().pk
            except AttributeError:
                return reverse_lazy('addtest', kwargs={'slug': course.slug})
            
            return reverse_lazy('updatetest', kwargs={'slug': course.slug, 'pk': pk})
    
class UpdateTest(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    template_name = 'updateTest.html'
    form_class = TestForm
    model = Test

    def dispatch(self, request, *args, **kwargs):
        try:
            Teacher.objects.get(user=request.user)
        except:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        user = Teacher.objects.get(user=self.request.user)
        courses = Course.objects.filter(teacher=user)
        kwargs['teacher_courses'] = courses
        return kwargs
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(slug=self.kwargs['slug'])
        context['test'] = Test.objects.get(id=self.kwargs['pk'])
        return context

    def form_invalid(self, form):
        error_msg_dict = json.loads(form.errors.as_json())
        error = test_validate(error_msg_dict)
        return render(self.request, self.template_name, {'form': form, 'error': error})
    
    def get_success_url(self):
        form = self.request.POST
        course = Course.objects.get(slug=self.kwargs['slug'])
        # add_more takes to another test
        if form.get('add_more'):
            next_test = get_next_test(course,self.kwargs['pk'])
            if not next_test:
                return reverse('addtest', kwargs={'slug': course.slug})
            else:
                return reverse('updatetest', kwargs={'slug': course.slug, 'pk': next_test.pk})
        # publish takes to dashboard
        if form.get('publish'):
            return '/teacher/dashboard/'
        

class DeleteCourse(DeleteView):
    model = Course
    success_url = reverse_lazy('teacher_dashboard')

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)

    def post(self, request, *args, **kwargs): 
        self.object = self.get_object() 
        self.object.delete() 
        return redirect(self.success_url)
    

class DeleteChapter(DeleteView):
    model = Chapter

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
    
    def get_success_url(self):
        course = Course.objects.get(slug=self.kwargs['slug'])
        next_chapter = get_next_chapter(course,self.kwargs['pk'])
        if not next_chapter:
            return reverse('updatecourse', kwargs={'slug': course.slug})
        else:
            return reverse('updatechapter', kwargs={'slug': course.slug, 'pk': next_chapter.pk})
    
    def post(self,request, *args, **kwargs):
        self.object = self.get_object() 
        self.object.delete() 
        return redirect(self.get_success_url())
    
class DeleteTest(DeleteView):
    model = Test

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
    
    def get_success_url(self):
        course = Course.objects.get(slug=self.kwargs['slug'])
        chapter = Chapter.objects.filter(course=course).first()
        next_test = get_next_test(course,self.kwargs['pk'])
        if not next_test:
            return reverse('updatechapter', kwargs={'slug': course.slug,'pk':chapter.pk})
        else:
            return reverse('updatetest', kwargs={'slug': course.slug, 'pk': next_test.pk})
    
    def post(self,request, *args, **kwargs):
        self.object = self.get_object() 
        self.object.delete() 
        return redirect(self.get_success_url())