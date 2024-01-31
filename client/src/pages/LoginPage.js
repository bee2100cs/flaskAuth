import React, { useState }from 'react';
import httpClient from '../httpClient';


const LoginPage = () => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    // Make an http request to the API
    const logInUser = async () => {
        console.log(password)

        try{
            const resp = await httpClient.post("//localhost:5000/login", {
                email,
                password,
            });

            // Return to the homepage
            window.location.href = "/";
        } catch (error) {
            if (error.response.status === 401) {
                alert("Invalid Credentials")
            }
        }
    
        
    };
  return (
    <div>
        <h1>Log Into Your Account</h1>
        <form>
            <div>
            <label htmlFor="email">Email: </label>
            <input 
            type="email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            id="email" />
            </div>
            <div>
            <label htmlFor="password">Password: </label>
            <input 
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            id="password" />
            </div>
            <button type="button" onClick={ () => logInUser() }>
                Submit
            </button>
        </form>
    </div>
  )
}

export default LoginPage