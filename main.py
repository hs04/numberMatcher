import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
import firebase_admin
from firebase_admin import credentials,db

json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'testing-project-1-42371-firebase-adminsdk-dgxww-d3de4a33b9.json')
cred = credentials.Certificate(json_path)
firebase_admin.initialize_app(cred,{'databaseURL': 'https://testing-project-1-42371-default-rtdb.asia-southeast1.firebasedatabase.app/'})
ref = db.reference('/user_data')

class MyApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        self.name_input = TextInput(hint_text='Enter your name', multiline=False)
        self.number_input = TextInput(hint_text='Enter a number', multiline=False)
        submit_button = Button(text='Submit', on_press=self.submit_data)
        
        
        self.result_label = Label(text='', halign='left', valign='top', markup=True)

        self.layout.add_widget(self.name_input)
        self.layout.add_widget(self.number_input)
        self.layout.add_widget(submit_button)
        self.layout.add_widget(self.result_label)
        
        
        return self.layout

    def submit_data(self, instance):
        user_name = self.name_input.text
        user_number = float(self.number_input.text)

        new_user_ref = ref.push()  # Generate a unique key for each user
        new_user_ref.set({
            'name': user_name,
            'number': user_number
        })

        # Clear input fields after submission
        self.name_input.text = ''
        self.number_input.text = ''
        print('Data submitted successfully!')

        self.result_label.text = "Submitted data succesfully for "+user_name

        data = ref.get()
        print(data.values())
        #sorted_users = sorted(data, key=lambda x: abs(x['number'] - user_number))
        #print(sorted_users)

        users_proximity = [{'Name': user_data['name'], 'proximity': abs(float(user_data['number']) - user_number)} for user_id, user_data in data.items() if 'number' in user_data]
        
        sorted_users = sorted(users_proximity, key=lambda x: x['proximity'])

        top_3_users = sorted_users[1:4]
        print(top_3_users)

        proximity_string = ''
        for i in top_3_users:
                proximity_string += '\nName of Person : '+i['Name']+' ; Distance from your input number : '+str("%.3f"%i['proximity'])
        
        self.result_label.text = "Hi "+user_name+", here are the top 3 people closest to you :"+proximity_string



    def back_to_main_screen(self, instance):
        # Clear the result label and reset the input field
        self.result_label.text = ''
        self.number_input.text = ''

if __name__ == '__main__':
    MyApp().run()
