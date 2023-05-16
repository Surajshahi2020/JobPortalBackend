from rest_framework import serializers
from login.models import Payment, Job, VerifyPayment
import requests as req
from datetime import datetime


class KhaltiPaymentSerializer(serializers.ModelSerializer):
    khalti = serializers.SerializerMethodField()
    job_title = serializers.SerializerMethodField()

    def get_job_title(self, obj: Payment):
        return obj.job.title

    def get_khalti(self, obj):
        initiate_url = "https://a.khalti.com/api/v2/epayment/initiate/"

        headers = {
            "Authorization": "Key dcbee64c6f8a47ffa81d7f643d583204",
            "Content-Type": "application/json",
        }

        amount = obj.amount * 100
        data = {
            "purchase_order_id": str(obj.job.id),
            "amount": f"{amount}",
            "return_url": "http://localhost:8000/api/v1/payment/make-payment/",
            "purchase_order_name": f"My-{obj.job.title}",
            "website_url": "http://localhost:8000/",
        }

        verification_response = req.post(
            initiate_url, json=data, headers=headers
        ).json()

        return verification_response

    class Meta:
        model = Payment
        fields = [
            "student",
            "job",
            "apply_date",
            "amount",
            "job_title",
            "khalti",
        ]


class KhaltiPaymentVerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = VerifyPayment
        fields = [
            "reference_code",
        ]

    def create(self, validated_data):
        pidx = validated_data.get("reference_code")
        url = "https://a.khalti.com/api/v2/epayment/lookup/"
        headers = {
            "Authorization": "Key dcbee64c6f8a47ffa81d7f643d583204",
            "Content-Type": "application/json",
        }

        data = {
            "pidx": pidx,
        }
        response = req.post(url, headers=headers, json=data)
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get("status") == "completed":
                return super().create(validated_data)
            else:
                raise serializers.ValidationError(
                    {
                        "title": "Pidx validation",
                        "message": "Response status is not completed",
                    }
                )
        else:
            raise serializers.ValidationError(
                {
                    "title": "Pidx validation",
                    "message": "Unexpected response status: "
                    + str(response.status_code),
                }
            )
