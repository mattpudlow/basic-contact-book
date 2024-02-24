import { useState, useEffect } from 'react'
import ContactList from './ContactList'
import ContactForm from './ContactForm'
import './App.css'

function App() {
  const [contacts, setContacts] = useState([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [currentContact, setCurrentContact] = useState({})
  const [searchQuery, setSearchQuery] = useState([])

  useEffect(() => {
    fetchContacts()
  }, [searchQuery])

  const fetchContacts = async () => {
    let url = 'http://127.0.0.1:5000/contacts'
    if (searchQuery) {
      url += `?query=${searchQuery}`
    }
    const response = await fetch(url)
    const data = await response.json()
    setContacts(data.contacts)
  }

  const closeModal = () => {
    setIsModalOpen(false)
    setCurrentContact({})
  }

  const openCreateModal = () => {
    if (!isModalOpen) setIsModalOpen(true)
  }

  const openEditModal = (contact) => {
    if (isModalOpen) return
    setCurrentContact(contact)
    setIsModalOpen(true)
  }

  const onUpdate = () => {
    closeModal()
    fetchContacts()
  }

  const handleSearch = (e) => {
    fetchContacts()
  }

  const handleInputChange = (e) => {
    setSearchQuery(e.target.value)
  }

  return <>
    <div className="search-container">
        <input type="text" className="search-input" placeholder="Search..." value={searchQuery} onChange={handleInputChange} />
        <button className="search-button" onClick={handleSearch}>Search</button>
      </div>
    <ContactList contacts={contacts} updateContact={openEditModal} updateCallback={onUpdate}/>
    <button onClick={openCreateModal}>Create Contact</button>
    {isModalOpen && <div className="modal">
      <div className="modal-content">
        <span className="close" onClick={closeModal}>&times;</span>
        <ContactForm existingContact={currentContact} updateCallback={onUpdate} />
        </div>
        </div>
    }
    </>
}

export default App
