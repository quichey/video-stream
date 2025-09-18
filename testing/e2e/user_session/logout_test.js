class LogOut {
      logOut() {
        cy.get('[data-testid="logout-menu-item"]').click();
        cy.get('[data-testid="view-channel-menu-item"]').should('not.exist');
      }

      runSuite() {
        this.logOut()
      }
}