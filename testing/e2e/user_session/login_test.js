class LoginTests {
    constructor(username, password) {
        this.username = username;
        this.password = password;
      }

      openDialog() {
        cy.get('[data-testid="login-menu-item"]').click();
        cy.get('[data-testid="login-dialogue"]').should('be.visible');
      }

      submit() {
        cy.get('[data-testid="login-name"]').type(this.username);
        cy.get('[data-testid="login-password"]').type(this.password);
        cy.get('[data-testid="login-submit"]').click();
        //cy.url().should('include', '/dashboard');
        // TODO: check that user's name is visible in Session Popover
        cy.get('[data-testid="view-channel-menu-item"]')
            .should('be.visible')
            .and('contain.text', this.username);
      }

      runSuite() {
        this.openDialog()
        this.submit()
      }
}