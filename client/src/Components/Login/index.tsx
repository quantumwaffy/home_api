import {FC} from "react"
import TextField from "@mui/material/TextField/TextField";
import FormControl from "@mui/material/FormControl";
import Button from "@mui/material/Button";
import LoginIcon from '@mui/icons-material/Login';
import "./style.css"

const Login: FC  = () => {
    return (
        <FormControl className="login-form-wrapper">
            <TextField
                className="login-form-element-wrapper"
                required
                label="Login"
                name="login"
            />
            <TextField
                className="login-form-element-wrapper"
                required
                label="Password"
                name="password"
            />
            <Button className="login-form-element-wrapper" color="secondary" variant="contained" endIcon={<LoginIcon />}>Login</Button>
        </FormControl>

    )
}
export default Login;