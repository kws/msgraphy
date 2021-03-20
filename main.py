
from msgraphy.data.user import User
from examples.sample_session_config import api


user: User = api.user.get_user_by_email("kaj.siebert@socialfinance.org.uk")
print(user)

drive = api.user.get_user_drive(user)

name = ["Data", "Data/Projects - Time and Costs.xlsx", "user research tools - orig.png"]
for n in name:
    file = api.files.get_file_by_name(drive, n)
    print(file)