
export function logInTests({ username, password }) {
  describe('login Tests', () => {
    it('should open login dialogue', () => {
      cy.get('[data-testid="login-menu-item"]').click();
      cy.get('[data-testid="login-dialogue"]').should('be.visible');
    });
    it('should login', () => {
      cy.get('[data-testid="login-name"]').type(username);
      cy.get('[data-testid="login-password"]').type(password);
      cy.get('[data-testid="login-submit"]').click();
      //cy.url().should('include', '/dashboard');
      // TODO: check that user's name is visible in Session Popover
      cy.get('[data-testid="view-channel-menu-item"]')
        .should('be.visible')
        .and('contain.text', username);
    });
  });
}
export function logOut() {
  describe('log Out', () => {
    it('should logout', () => {
      cy.get('[data-testid="logout-menu-item"]').click();
      cy.get('[data-testid="view-channel-menu-item"]').should('not.exist');
    });
  });
}
export function registerUser({ username, password }) {
  describe('register Tests', () => {
    it('should open register dialogue', () => {
      cy.get('[data-testid="register-menu-item"]').click();
      cy.get('[data-testid="register-dialogue"]').should('be.visible');
    });
    it('should register', () => {
      cy.get('[data-testid="register-name"]').type(username);
      cy.get('[data-testid="register-password"]').type(password);
      cy.get('[data-testid="register-submit"]').click();
      //cy.url().should('include', '/dashboard');
      // TODO: check that user's name is visible in Session Popover
      cy.get('[data-testid="view-channel-menu-item"]')
        .should('be.visible')
        .and('contain.text', username);
    });
  });
}
export function openSessionMenu() {
  describe('session menu Tests', () => {
    it('should open', () => {
      cy.get('[data-testid="session-menu-btn"]').click();
      cy.get('[data-testid="session-menu-popover"]').should('be.visible');
    });
  });
}