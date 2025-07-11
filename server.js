// server.js
const express = require('express');
const nodemailer = require('nodemailer');

const app = express();
app.use(express.json());

// Replace these with your Gmail and App Password (no spaces in the password)
const GMAIL_USER = 'your.email@gmail.com';
const GMAIL_APP_PASSWORD = 'cbibth35oy33ocjb'; // your 16-char app password without spaces

const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: GMAIL_USER,
    pass: GMAIL_APP_PASSWORD
  }
});

app.post('/contact', (req, res) => {
  const { email, message } = req.body;

  const mailOptions = {
    from: GMAIL_USER,
    to: GMAIL_USER,  // your Gmail to receive emails
    subject: 'New Contact Form Submission',
    text: `Email: ${email}\nMessage: ${message}`
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      console.error('Error sending email:', error);
      return res.status(500).send('Error sending email');
    }
    console.log('Email sent:', info.response);
    res.send('Email sent successfully');
  });
});

const PORT = 9465;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
