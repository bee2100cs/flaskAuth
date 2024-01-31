import React, {useState, useEffect} from 'react';
import httpClient from '../httpClient';
const LandingPage = () => {
    const [user, setUser] = useState(null);

    const logoutUser = async () => {
        await httpClient.post("//localhost:5000/logout");
        window.location.href = "/";
    }
    useEffect(() => {
        (async () => {
            try {
                const resp = await httpClient.get("//localhost:5000/@me");
                
                setUser(resp.data);
            } catch (error) {
                console.log("not authenticated");
            } 
        })();
    }, []);
    return (<div>
        <h1>Welcome To This Login App</h1>
        {user != null ? (
            <div>
                <h2>Logged In</h2>
                <h3>Email: {user.email}</h3>
                <h3>ID: {user.id}</h3>

                <button onClick={logoutUser}>Log Out</button>
            </div>
            
        ) : ( 
            <div>
                <p>You are not logged in</p>
                <div >
                    <a href='/login'>
                        <button>Login</button>
                    </a>
                    <a href='/signup'>
                        <button>Signup</button>
                    </a>
                </div>
            </div>
        )}
    </div>
    );
};

export default LandingPage;