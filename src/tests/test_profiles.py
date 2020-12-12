import unittest
from main import create_app, db
from models.Profile import Profile
from models.User import User

class TestProfiles(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.app = create_app()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()
        cls.client = cls.app.test_client()
        db.create_all()
        runner = cls.app.test_cli_runner()
        runner.invoke(args=["db", "seed"])

    @classmethod
    def tearDown(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()




    def test_profiles_index(self):
        response= self.client.get("/profile/")

        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)

    def test_profile_create(self):
        response = self.client.post("/auth/register",                   
        json = {                                                        
            "email": "test1@test.com",
            "password": "123456"
        })
        response = self.client.post("/auth/login",                      
        json = {              
            "email": "test1@test.com",
            "password": "123456"
        })                    
        data = response.get_json()                                      
        headers_data= {                                                 
            'Authorization': f"Bearer {data['token']}"
        }
        data = {                                                       
            "username" : "test_username", 
            "fname" : "test", 
            "lname" : "test",
            "account_active": "True"
        }
        response = self.client.post("/profile/",                       
        json = data,                                                    
        headers = headers_data)                                         
        self.assertEqual(response.status_code, 200)                     
        data = response.get_json()                                      
        profile = Profile.query.get(data["user"]["id"])                 
        self.assertIsNotNone(profile)                                   
        self.assertEqual(profile.username, "test_username") 

    # def test_user_update(self):
    #     response = self.client.post("/users/", json=  {
    #         "account_active": "False",
    #         "email": "Test Email2",
    #         "fname": "Test Fname2",
    #         "lname": "Test Lname2",
    #         "profile_pic": "Test Pic2",
    #         "username": "Test_username2",
    #         "userpass": "Test_Pass2",
    #         })

        

    #     responseput = self.client.put("/users/Test_username2", json=  {
    #         "account_active": "False",
    #         "email": "Updated",
    #         "fname": "Updated",
    #         "lname": "Updated",
    #         "profile_pic": "Test Pic2",
    #         "username": "Updated",
    #         "userpass": "Test_Pass2",
    #         }) 

    #     data = responseput.get_json()

    #     #self.assertEqual(response.status_code, 200)
    #     self.assertTrue(bool(response.status_code >= 200 and response.status_code < 300))
    #     self.assertIsInstance(data, dict)
    #     self.assertTrue(bool("userid" in data.keys()))
    #     self.assertEqual(data["username"] == username)

    #     user = Users.query.get(data["userid"])
    #     self.assertIsNotNone(user)

    # def test_book_delete(self):
    #     profile = Profile.query.filter_by(username = username, user_id=user.id).first()

    #     response = self.client.delete(f"/profile/{profile.username}")
    #     data = response.get_json()

    #     self.assertEqual(response.status_code, 200)

    #     profile = Profile.query.get(profile.profileid)
    #     self.assertIsNone(profile)