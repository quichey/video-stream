def test_app_fixture_connects_to_test_db(client, app):
    """
    Integration check: Ensures the app's Orchestrator registers sessions
    and those sessions are wired to the SQLite test DB.
    """
    # 1. Use the 'with' context to keep the session state alive
    with client:
        # Trigger the Orchestrator logic
        client.post("/video-list")

        # 2. Access the registry via the app object
        # Since the Orchestrator is a singleton-like object on the app,
        # it should now contain the session created during client.get("/")
        orchestrator = app.client_router.orchestrator
        registry = orchestrator.SESSION_MANAGEMENT.SESSION_REGISTRY.sessions

        # Verify the session was registered
        assert len(registry) > 0, "The Orchestrator did not register a session!"

        # 3. Deep Inspect the BrowserSession's database engine
        # Grab the first session in the registry
        session_id = list(registry.keys())[0]
        browser_session = registry[session_id]

        engine_url = str(browser_session.engine.url)
        print(f"\n[PROBE] Session {session_id} Engine: {engine_url}")

        # Final Verification: Ensure we are NOT on MySQL/Azure
        assert "sqlite" in engine_url, f"FAIL: Session using non-test DB: {engine_url}"
        assert "test_gateway.sqlite" in engine_url
