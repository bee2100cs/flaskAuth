import { BrowserRouter, Routes, Route } from "react-router-dom";
import LandingPage from "./pages/LandingPage";
import NotFound from "./pages/NotFound";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
const Router = () => {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/"  element={< LandingPage />}/>
                <Route path="/login" element={< LoginPage />} />
                <Route path="/signup" element={< SignupPage />} />
                <Route path="*" element={< NotFound />} />
                
            </Routes>
        </BrowserRouter>
    )
}

export default Router;
