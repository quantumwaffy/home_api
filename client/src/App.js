import './App.css';
import Login from "./Components/Login/index.tsx";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  return (
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
       <Login/>
      </ThemeProvider>
  );
}

export default App;
