class SessionMenu {
      open() {
        cy.get('[data-testid="session-menu-btn"]').click();
        cy.get('[data-testid="session-menu-popover"]').should('be.visible');
      }

      runSuite() {
        this.open()
      }
}