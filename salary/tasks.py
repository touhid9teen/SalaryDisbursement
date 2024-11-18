from celery import shared_task
from users.models import Users
from .models import SalaryDisbursement, SalaryBeneficiary


@shared_task
def update_Salary_Disbursement(content):
    print("TASKS CALLED ")
    print("content = ", content)
    update_count = 0
    for field_ in content:
        try:
            employ_instance = Users.objects.get(id=field_.get("employ"))
            beneficiary_instance = SalaryBeneficiary.objects.get(id=field_.get("beneficiary_id"))
            SalaryDisbursement.objects.create(
                employ = employ_instance,
                wallet_no = field_.get("wallet_no"),
                amount = field_.get("amount"),
                beneficiary_id = beneficiary_instance,
            )
            update_count += 1  # Increment on successful update
        except Users.DoesNotExist:
            print(f"User with ID {field_.get('employ')} not found.")
        except SalaryBeneficiary.DoesNotExist:
            print(f"Beneficiary with ID {field_.get('beneficiary_id')} not found.")

    return f"Processed {update_count} salary disbursements."


# celery -A myproject worker --loglevel=info
