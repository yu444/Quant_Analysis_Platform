import React, { useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';

const PageContainer = styled.div`
  background-image: url('/analysis-background.jpg');
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
`;

const IconContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
`;

const Icon = styled.img`
  width: 80px;
  height: 80px;
  margin-bottom: 16px;
`;

const Title = styled.h2`
  color: #ffffff;
  font-size: 28px;
  margin-bottom: 24px;
  text-align: center;
`;

const Form = styled.form`
  background-color: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(5px);
  padding: 32px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
`;

const FormGroup = styled.div`
  margin-bottom: 20px;
`;

const Label = styled.label`
  display: block;
  margin-bottom: 8px;
  color: #ffffff;
  font-weight: bold;
`;

const Input = styled.input`
  width: 100%;
  padding: 10px;
  background-color: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 4px;
  font-size: 16px;
  color: #ffffff;

  &::placeholder {
    color: rgba(255, 255, 255, 0.7);
  }
`;

const Button = styled.button`
  width: 100%;
  padding: 12px;
  background-color: #1e40af;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;

  &:hover {
    background-color: #1e3a8a;
  }
`;

const Message = styled.p`
  margin-top: 16px;
  color: ${props => props.error ? '#ff6b6b' : '#51cf66'};
  font-weight: bold;
`;

function Login() {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState(false);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const checkAuth = async () => {
    try {
      const response = await fetch('http://localhost:5000/check_auth', {
        method: 'GET',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) throw new Error('Auth check failed');
      
      const data = await response.json();
      return data.message === 'Authenticated';
    } catch (error) {
      console.error('Auth check failed:', error);
      return false;
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    setError(false);
  
    try {
      console.log("Login started");
      
      // Add timeout promise
      const loginPromise = fetch('http://localhost:5000/login', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });
  
      // Create timeout promise
      const timeoutPromise = new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Request timed out')), 5000)
      );
  
      // Race between login request and timeout
      const response = await Promise.race([loginPromise, timeoutPromise]);
      console.log("Response received");
      
      const data = await response.json();
      console.log("Response data:", data);
  
      if (!response.ok) {
        throw new Error(data.message || 'Login failed');
      }
  
      setMessage(data.message);
      console.log("Login successful, navigating to dashboard");
      // Remove the checkAuth call and directly navigate on successful login
      navigate('/dashboard');
      
    } catch (error) {
      console.error("Login error:", error);
      setError(true);
      setMessage(error.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageContainer>
      <Container>
        <IconContainer>
          <Icon src="/quant_analysis_icon.png" alt="Analysis Icon" />
          <Title>Log in to your account</Title>
        </IconContainer>
        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label htmlFor="username">Username</Label>
            <Input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleChange}
              required
              placeholder="Enter your username"
              disabled={loading}
            />
          </FormGroup>
          <FormGroup>
            <Label htmlFor="password">Password</Label>
            <Input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              required
              placeholder="Enter your password"
              disabled={loading}
            />
          </FormGroup>
          <Button type="submit" disabled={loading}>
            {loading ? 'Logging in...' : 'Log In'}
          </Button>
        </Form>
        {message && <Message error={error}>{message}</Message>}
      </Container>
    </PageContainer>
  );
}

// Your existing styled components remain the same

export default Login;