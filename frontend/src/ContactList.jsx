import React, { useState } from 'react';

const ContactList = ({ contacts, updateContact, updateCallback }) => {
  const [sortCriteria, setSortCriteria] = useState(null);
  const [sortOrder, setSortOrder] = useState('asc'); // Default sorting order: ascending

  const onDelete = async (id) => {
    try {
      const options = { method: "DELETE" };
      const response = await fetch(`http://127.0.0.1:5000/delete_contact/${id}`, options);
      if (response.status === 200) {
        updateCallback();
      } else {
        console.error(response.status, "Failed to delete contact");
      }
    } catch (error) {
      alert(error);
    }
  };

  const handleSort = (criteria) => {
    if (sortCriteria === criteria) {
      // Toggle sorting order if sorting by the same criteria
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      // Set new sorting criteria and reset sorting order to default (ascending)
      setSortCriteria(criteria);
      setSortOrder('asc');
    }
  };

  const sortedContacts = [...contacts].sort((a, b) => {
    // Sort contacts based on the selected criteria and order
    if (sortCriteria) {
      const aValue = a[sortCriteria].toLowerCase();
      const bValue = b[sortCriteria].toLowerCase();
      if (sortOrder === 'asc') {
        return aValue.localeCompare(bValue);
      } else {
        return bValue.localeCompare(aValue);
      }
    }
    return 0; // No sorting applied
  });

  return (
    <div>
      <h2>Contact List</h2>
      <table>
        <thead>
          <tr>
            <th>
              <button onClick={() => handleSort('firstName')}>First Name</button>
            </th>
            <th>
              <button onClick={() => handleSort('lastName')}>Last Name</button>
            </th>
            <th>
              <button onClick={() => handleSort('email')}>Email</button>
            </th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {sortedContacts.map((contact) => (
            <tr key={contact.id}>
              <td>{contact.firstName}</td>
              <td>{contact.lastName}</td>
              <td>{contact.email}</td>
              <td>
                <button onClick={() => updateContact(contact)}>Update</button>
                <button onClick={() => onDelete(contact.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ContactList;
