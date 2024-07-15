from rest_framework import serializers
import requests
from .models import Student,CoursePayment
from course.models import Course
class VerifyPaymentSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    amount = serializers.IntegerField(required=True)

    def validate(self, attrs):
        token = attrs.get('token')
        amount = attrs.get('amount')
        product_url = attrs.get('product_url')


        url = "http://127.0.0.1:8000/khalti/verifypayment/"

        payload = {
            'token':token,
            'amount':amount
        }

        headers = {
            'Authorization': 'key test_public_key_c41fa2f081e44957809cd4bf0e2496eb',
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        attrs['response'] = response

        print(response.text)

        user = self.context['request'].user
        student = Student.objects.get(user=user)
        # print(response.json())
        course = Course.objects.get(id=response.json()['details']['product_identity'])

        course_payement = CoursePayment.objects.create(student=student, course=course,amount=amount)
        attrs['course_payement'] = product_url

        return attrs