import { logInTests, logOut, registerUser, openSessionMenu } from ".";


export function runSessionTests({ username, password }) {
    openSessionMenu();
    registerUser({username, password});
    logOut();
    logInTests({username, password});
}    