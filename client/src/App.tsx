import React from 'react';
import Login from "./Components/Login/index";
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import {Provider} from 'react-redux';
import store from './store/store'

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

function App() {
  return (
      <Provider store={store}>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
       <Login/>
      </ThemeProvider>
      </Provider>
  );
}

export default App;
