
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
      cy.get('input[name="username"]').type(username);
      cy.get('input[name="password"]').type(password);
      cy.get('button[type="submit"]').click();
      cy.url().should('include', '/dashboard');
    });
  });
}
export function registerUser({ username, password }) {
  describe('register Tests', () => {
    it('should register', () => {
      cy.get('input[name="username"]').type(username);
      cy.get('input[name="password"]').type(password);
      cy.get('button[type="submit"]').click();
      cy.url().should('include', '/dashboard');
    });
  });
}
export function openSessionMenu({ username, password }) {
  describe('session menu Tests', () => {
    it('should open', () => {
      cy.get('[data-testid="session-menu-btn"]').click();
      cy.get('[data-testid="session-menu-popover"]').should('be.visible');
    });
  });
}
describe('User can register', () => {
  const BASE_URL = 'http://localhost:3000'; // or your deployed URL

  it('should load the homepage', () => {
    cy.visit(BASE_URL);
    cy.contains('Copy-Youtube'); // check page title or header
  });

  it('should display video thumbnails within reasonable time', () => {
    cy.visit(BASE_URL);

    // Wait up to 10 seconds for the video list to appear
    cy.get('[data-testid=video-list]', { timeout: 10000 }).should('exist');

    // Make sure at least one video thumbnail is loaded
    cy.get('[data-testid=video-item]').should('have.length.greaterThan', 0);
  });

  it('should load the first video when clicked', () => {
    cy.visit(BASE_URL);

    // Click on the first video
    cy.get('[data-testid=video-item]').first().click();

    // Check that the video player appears
    cy.get('[data-testid=video-player]', { timeout: 10000 }).should('be.visible');

    // Optional: check that video metadata (title, description) is visible
    cy.get('[data-testid=video-title]').should('not.be.empty');
  });

  it('should load video within acceptable time', () => {
    cy.visit(BASE_URL);

    cy.get('[data-testid=video-item]').first().click();

    // Ensure video element starts playing within 10 seconds
    cy.get('[data-testid=video-player]', { timeout: 10000 }).should(($video) => {
      const video = $video[0];
      expect(video.readyState).to.be.gte(2); // HAVE_CURRENT_DATA
    });
  });
});
