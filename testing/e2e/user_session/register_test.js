class RegisterTests {
    constructor(username, password) {
        this.username = username;
        this.password = password;
      }

      openDialog() {
        cy.get('[data-testid="register-menu-item"]').click();
        cy.get('[data-testid="register-dialogue"]').should('be.visible');
      }

      submit() {
        cy.get('[data-testid="register-name"]').type(username);
        cy.get('[data-testid="register-password"]').type(password);
        cy.get('[data-testid="register-submit"]').click();
        //cy.url().should('include', '/dashboard');
        // TODO: check that user's name is visible in Session Popover
        cy.get('[data-testid="view-channel-menu-item"]')
            .should('be.visible')
            .and('contain.text', username);
      }

      runSuite() {
        this.openDialog()
        this.submit()
      }
}