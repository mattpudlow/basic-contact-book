from flask import request, jsonify
from config import app, db
from models import Contact


@app.route('/contacts', methods=['GET'])
def get_contacts():
    search_query = request.args.get('query')
    sort_criteria = request.args.get('sort')
    query = Contact.query

    if search_query:
        query = query.filter(
            (Contact.first_name.contains(search_query)) |
            (Contact.last_name.contains(search_query)) |
            (Contact.email.contains(search_query))
        )
    
    if sort_criteria:
        if sort_criteria == 'first_name':
            query = query.order_by(Contact.first_name)
        elif sort_criteria == 'last_name':
            query = query.order_by(Contact.last_name)
        elif sort_criteria == 'email':
            query = query.order_by(Contact.email)

    contacts = query.all()
    json_contacts = list(map(lambda contact: contact.to_json(), contacts))
    return jsonify({'contacts': json_contacts})

@app.route('/create_contact', methods=['POST'])
def create_contact():
    first_name = request.json.get('firstName')
    last_name = request.json.get('lastName')
    email = request.json.get('email')

    if not first_name or not last_name or not email:
        return jsonify({'error': 'Please provide first name, last name and email'}), 400
    
    new_contact = Contact(first_name=first_name, last_name=last_name, email=email)
    try:
        db.session.add(new_contact)
        db.session.commit()
        return jsonify({'message': 'Contact created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    
@app.route('/update_contact/<int:user_id>', methods=['PATCH'])
def update_contact(user_id):
    contact = Contact.query.get(user_id)
    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    
    contact.first_name = request.json.get('firstName', contact.first_name)
    contact.last_name = request.json.get('lastName', contact.last_name)
    contact.email = request.json.get('email', contact.email)

    try:
        db.session.commit()
        return jsonify({'message': 'Contact updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


@app.route('/delete_contact/<int:user_id>', methods=['DELETE'])
def delete_contact(user_id):
    contact = Contact.query.get(user_id)

    if not contact:
        return jsonify({'error': 'Contact not found'}), 404
    
    try:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Contact deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()


    app.run(debug=True)
    


