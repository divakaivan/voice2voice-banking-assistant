# from config.settings import DatabaseConfig, EngineConfig

# def test_database_config(monkeypatch):
#     monkeypatch.setenv("DB_NAME", "testdb")
#     monkeypatch.setenv("DB_USER", "testuser")
#     monkeypatch.setenv("DB_PASSWORD", "testpassword")
#     monkeypatch.setenv("DB_HOST", "testhost")
#     monkeypatch.setenv("DB_PORT", "5433")

#     config = DatabaseConfig()

#     assert config.name == "testdb", "Database name should be 'testdb'"
#     assert config.user == "testuser", "Database user should be 'testuser'"
#     assert config.password == "testpassword", "Database password should be 'testpassword'"
#     assert config.host == "testhost", "Database host should be 'testhost'"
#     assert config.port == "5433", "Database port should be '5433'"
    
#     expected_conninfo = "dbname=testdb user=myuser password=testpassword host=testhost port=5433"
#     assert config.conninfo == expected_conninfo, f"Connection info should be {expected_conninfo}"


# def test_engine_config(monkeypatch):
#     test_groq_key = "test_groq_key"
#     test_openai_key = "test_openai_key"
#     monkeypatch.setenv("GROQ_API_KEY", test_groq_key)
#     monkeypatch.setenv("OPENAI_API_KEY", test_openai_key)

#     config = EngineConfig()

#     assert config.GROQ_API_KEY == "test_groq_key", f"GROQ API key should be {test_groq_key}"
#     assert config.OPENAI_API_KEY == "test_openai_key", f"OpenAI API key should be {test_openai_key}"

