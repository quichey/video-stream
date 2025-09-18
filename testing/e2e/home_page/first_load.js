class FirstLoad {
  #BASE_URL = 'http://localhost:3000'; // or your deployed URL

  loadHomePage() {
    cy.visit(this.#BASE_URL);
    //cy.contains('Copy-Youtube'); // check page title or header
    cy.contains('Search'); // check page title or header
  };

  loadVideos() {
    // Wait up to 10 seconds for the video list to appear
    cy.get('[data-testid=home-videos-list]', { timeout: 10000 }).should('exist');

    // Make sure at least one video thumbnail is loaded
    cy.get('[data-testid=home-video-list-item]').should('have.length.greaterThan', 0);
  };

  navigateToWatchVideo(video_name) {
    // Click on the first video
    cy.get('[data-testid=home-video-list-item]').first().click();

    // Check that the video player appears
    cy.get('[data-testid=video-player]', { timeout: 10000 }).should('be.visible');

    cy.get('video[data-testid="video-player"]').then($video => {
    const video = $video[0];
        expect(video.duration).to.be.greaterThan(0); // TODO: get precise duration of video?
    });
  };

      runSuite() {
        this.open()
        this.loadVideos()
        this.navigateToWatchVideo()
      }
}