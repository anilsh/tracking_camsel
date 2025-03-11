import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Data Models for Simulation
class Contact:
    def __init__(self, name, relation, phone_number):
        self.name = name
        self.relation = relation
        self.phone_number = phone_number

    def __str__(self):
        return f"{self.name} ({self.relation})"

class CallLog:
    def __init__(self, contact, duration, timestamp):
        self.contact = contact
        self.duration = duration
        self.timestamp = timestamp

    def __str__(self):
        return f"Call with {self.contact.name} ({self.duration} mins) on {self.timestamp}"

class MessageLog:
    def __init__(self, contact, message, timestamp):
        self.contact = contact
        self.message = message
        self.timestamp = timestamp

    def __str__(self):
        return f"Message from {self.contact.name}: '{self.message}' on {self.timestamp}"

# Simulate Contact Data
def generate_contacts():
    relations = ['Family', 'Friend', 'Colleague', 'Business']
    contacts = []
    
    for _ in range(10):
        name = fake.name()
        relation = random.choice(relations)
        phone_number = fake.phone_number()
        contact = Contact(name, relation, phone_number)
        contacts.append(contact)
    
    return contacts

# Simulate Call Logs
def generate_call_logs(contacts):
    call_logs = []
    for contact in contacts:
        num_calls = random.randint(5, 15)
        for _ in range(num_calls):
            duration = random.randint(3, 30)  # Call duration in minutes
            # Longer calls for family
            if contact.relation == 'Family':
                duration += random.randint(10, 20)
            timestamp = fake.date_this_year() + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
            call_log = CallLog(contact, duration, timestamp)
            call_logs.append(call_log)
    
    return call_logs

# Simulate Message Logs
def generate_message_logs(contacts):
    message_logs = []
    for contact in contacts:
        num_messages = random.randint(5, 20)
        for _ in range(num_messages):
            message_type = random.choice(['Formal', 'Informal', 'Friendly', 'Business'])
            # Custom messages based on relation
            if message_type == 'Formal':
                message = f"Hello, I would like to discuss the work-related matter with you."
            elif message_type == 'Informal':
                message = f"Hey! What's up?"
            elif message_type == 'Friendly':
                message = f"How's your day going? Let's catch up soon!"
            else:  # Business
                message = f"Please review the attached document, thank you."
            
            timestamp = fake.date_this_year() + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
            message_log = MessageLog(contact, message, timestamp)
            message_logs.append(message_log)
    
    return message_logs

# Convert data to Turtle format
def convert_to_ttl(contacts, call_logs, message_logs):
    ttl_data = []

    # Prefixes
    ttl_data.append("@prefix ex: <http://example.org/> .")
    ttl_data.append("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .")
    
    # Contacts
    for contact in contacts:
        ttl_data.append(f'ex:{contact.name.replace(" ", "")} a ex:Person ;')
        ttl_data.append(f'    ex:hasPhoneNumber "{contact.phone_number}" ;')
        ttl_data.append(f'    ex:hasRelation "{contact.relation}" ;')
        ttl_data.append(f'    ex:hasName "{contact.name}" .\n')
    
    # Call Logs
    for i, call_log in enumerate(call_logs):
        ttl_data.append(f'ex:CallLog{i+1} a ex:CallLog ;')
        ttl_data.append(f'    ex:hasContact ex:{call_log.contact.name.replace(" ", "")} ;')
        ttl_data.append(f'    ex:hasDuration "{call_log.duration}"^^xsd:int ;')
        ttl_data.append(f'    ex:hasTimestamp "{call_log.timestamp}"^^xsd:dateTime .\n')
    
    # Message Logs
    for i, message_log in enumerate(message_logs):
        ttl_data.append(f'ex:MessageLog{i+1} a ex:MessageLog ;')
        ttl_data.append(f'    ex:hasContact ex:{message_log.contact.name.replace(" ", "")} ;')
        ttl_data.append(f'    ex:hasMessage "{message_log.message}" ;')
        ttl_data.append(f'    ex:hasTimestamp "{message_log.timestamp}"^^xsd:dateTime .\n')
    
    return "\n".join(ttl_data)

# Simulate mobile data and convert to Turtle format
def simulate_and_generate_ttl():
    contacts = generate_contacts()
    call_logs = generate_call_logs(contacts)
    message_logs = generate_message_logs(contacts)

    ttl_content = convert_to_ttl(contacts, call_logs, message_logs)

    # Save the TTL data to a file
    with open("mobile_data.ttl", "w") as ttl_file:
        ttl_file.write(ttl_content)
    
    print("Turtle file 'mobile_data.ttl' generated successfully.")

# Run the simulation and generate TTL file
simulate_and_generate_ttl()



@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Contacts
ex:JohnDoe a ex:Person ;
    ex:hasPhoneNumber "+1234567890" ;
    ex:hasRelation "Family" ;
    ex:hasName "John Doe" .

ex:JaneSmith a ex:Person ;
    ex:hasPhoneNumber "+9876543210" ;
    ex:hasRelation "Friend" ;
    ex:hasName "Jane Smith" .

ex:AliceBrown a ex:Person ;
    ex:hasPhoneNumber "+1122334455" ;
    ex:hasRelation "Colleague" ;
    ex:hasName "Alice Brown" .

ex:BobJohnson a ex:Person ;
    ex:hasPhoneNumber "+9988776655" ;
    ex:hasRelation "Business" ;
    ex:hasName "Bob Johnson" .

# Call Logs
ex:CallLog1 a ex:CallLog ;
    ex:hasContact ex:JohnDoe ;
    ex:hasDuration "38"^^xsd:int ;
    ex:hasTimestamp "2025-03-02T15:23:00"^^xsd:dateTime .

ex:CallLog2 a ex:CallLog ;
    ex:hasContact ex:JaneSmith ;
    ex:hasDuration "22"^^xsd:int ;
    ex:hasTimestamp "2025-02-19T17:45:00"^^xsd:dateTime .

ex:CallLog3 a ex:CallLog ;
    ex:hasContact ex:AliceBrown ;
    ex:hasDuration "10"^^xsd:int ;
    ex:hasTimestamp "2025-01-15T14:30:00"^^xsd:dateTime .

ex:CallLog4 a ex:CallLog ;
    ex:hasContact ex:BobJohnson ;
    ex:hasDuration "15"^^xsd:int ;
    ex:hasTimestamp "2025-03-05T09:12:00"^^xsd:dateTime .

# Message Logs
ex:MessageLog1 a ex:MessageLog ;
    ex:hasContact ex:JohnDoe ;
    ex:hasMessage "How's your day going? Let's catch up soon!" ;
    ex:hasTimestamp "2025-02-10T11:22:00"^^xsd:dateTime .

ex:MessageLog2 a ex:MessageLog ;
    ex:hasContact ex:JaneSmith ;
    ex:hasMessage "Hello, I would like to discuss the work-related matter with you." ;
    ex:hasTimestamp "2025-03-08T14:12:00"^^xsd:dateTime .

ex:MessageLog3 a ex:MessageLog ;
    ex:hasContact ex:AliceBrown ;
    ex:hasMessage "How are you doing today? Catch up later!" ;
    ex:hasTimestamp "2025-01-17T09:55:00"^^xsd:dateTime .

ex:MessageLog4 a ex:MessageLog ;
    ex:hasContact ex:BobJohnson ;
    ex:hasMessage "Please review the attached document, thank you." ;
    ex:hasTimestamp "2025-03-01T10:45:00"^^xsd:dateTime .

import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Data Models for Simulation
class Contact:
    def __init__(self, name, relation, phone_number):
        self.name = name
        self.relation = relation
        self.phone_number = phone_number

    def __str__(self):
        return f"{self.name} ({self.relation})"

class CallLog:
    def __init__(self, contact, duration, timestamp):
        self.contact = contact
        self.duration = duration
        self.timestamp = timestamp

    def __str__(self):
        return f"Call with {self.contact.name} ({self.duration} mins) on {self.timestamp}"

class MessageLog:
    def __init__(self, contact, message, timestamp):
        self.contact = contact
        self.message = message
        self.timestamp = timestamp

    def __str__(self):
        return f"Message from {self.contact.name}: '{self.message}' on {self.timestamp}"

# Simulate Contact Data
def generate_contacts():
    relations = ['Family', 'Friend', 'Colleague', 'Business']
    contacts = []
    
    for _ in range(10):
        name = fake.name()
        relation = random.choice(relations)
        phone_number = fake.phone_number()
        contact = Contact(name, relation, phone_number)
        contacts.append(contact)
    
    return contacts

# Simulate Call Logs
def generate_call_logs(contacts):
    call_logs = []
    for contact in contacts:
        num_calls = random.randint(5, 15)
        for _ in range(num_calls):
            duration = random.randint(3, 30)  # Call duration in minutes
            # Longer calls for family
            if contact.relation == 'Family':
                duration += random.randint(10, 20)
            timestamp = fake.date_this_year() + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
            call_log = CallLog(contact, duration, timestamp)
            call_logs.append(call_log)
    
    return call_logs

# Simulate Message Logs
def generate_message_logs(contacts):
    message_logs = []
    for contact in contacts:
        num_messages = random.randint(5, 20)
        for _ in range(num_messages):
            message_type = random.choice(['Formal', 'Informal', 'Friendly', 'Business'])
            # Custom messages based on relation
            if message_type == 'Formal':
                message = f"Hello, I would like to discuss the work-related matter with you."
            elif message_type == 'Informal':
                message = f"Hey! What's up?"
            elif message_type == 'Friendly':
                message = f"How's your day going? Let's catch up soon!"
            else:  # Business
                message = f"Please review the attached document, thank you."
            
            timestamp = fake.date_this_year() + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
            message_log = MessageLog(contact, message, timestamp)
            message_logs.append(message_log)
    
    return message_logs

# Convert data to Turtle format
def convert_to_ttl(contacts, call_logs, message_logs):
    ttl_data = []

    # Prefixes
    ttl_data.append("@prefix ex: <http://example.org/> .")
    ttl_data.append("@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .")
    
    # Contacts
    for contact in contacts:
        ttl_data.append(f'ex:{contact.name.replace(" ", "")} a ex:Person ;')
        ttl_data.append(f'    ex:hasPhoneNumber "{contact.phone_number}" ;')
        ttl_data.append(f'    ex:hasRelation "{contact.relation}" ;')
        ttl_data.append(f'    ex:hasName "{contact.name}" .\n')
    
    # Call Logs
    for i, call_log in enumerate(call_logs):
        ttl_data.append(f'ex:CallLog{i+1} a ex:CallLog ;')
        ttl_data.append(f'    ex:hasContact ex:{call_log.contact.name.replace(" ", "")} ;')
        ttl_data.append(f'    ex:hasDuration "{call_log.duration}"^^xsd:int ;')
        ttl_data.append(f'    ex:hasTimestamp "{call_log.timestamp}"^^xsd:dateTime .\n')
    
    # Message Logs
    for i, message_log in enumerate(message_logs):
        ttl_data.append(f'ex:MessageLog{i+1} a ex:MessageLog ;')
        ttl_data.append(f'    ex:hasContact ex:{message_log.contact.name.replace(" ", "")} ;')
        ttl_data.append(f'    ex:hasMessage "{message_log.message}" ;')
        ttl_data.append(f'    ex:hasTimestamp "{message_log.timestamp}"^^xsd:dateTime .\n')
    
    return "\n".join(ttl_data)

# Simulate mobile data and convert to Turtle format
def simulate_and_generate_ttl():
    contacts = generate_contacts()
    call_logs = generate_call_logs(contacts)
    message_logs = generate_message_logs(contacts)

    ttl_content = convert_to_ttl(contacts, call_logs, message_logs)

    # Save the TTL data to a file
    with open("mobile_data.ttl", "w") as ttl_file:
        ttl_file.write(ttl_content)
    
    print("Turtle file 'mobile_data.ttl' generated successfully.")

# Run the simulation and generate TTL file
simulate_and_generate_ttl()
