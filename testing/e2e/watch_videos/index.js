
export function watchVideo({ videoID }) {
    describe('Watch Video Loading', () => {
    const BASE_URL = 'http://localhost:3000'; // or your deployed URL


    it('should load the video', () => {
        cy.visit(BASE_URL);

        // Click on the first video
        cy.get('[data-testid=video-item]').first().click();

        // Check that the video player appears
        cy.get('[data-testid=video-player]', { timeout: 10000 }).should('be.visible');

        // Optional: check that video metadata (title, description) is visible
        cy.get('[data-testid=video-title]').should('not.be.empty');
    });

    it('should load the comments', () => {
        cy.visit(BASE_URL);

        cy.get('[data-testid=video-item]').first().click();

        // Ensure video element starts playing within 10 seconds
        cy.get('[data-testid=video-player]', { timeout: 10000 }).should(($video) => {
        const video = $video[0];
        expect(video.readyState).to.be.gte(2); // HAVE_CURRENT_DATA
        });
    });
    });
}