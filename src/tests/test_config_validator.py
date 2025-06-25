"""Unit tests for configuration validation."""
import pytest
from ..utils.config_validator import ConfigValidator, ConfigurationError
import src.config.whatsapp as whatsapp  # Import module instead of constant

class TestConfigValidator:
    """Test cases for configuration validation"""
    
    def test_validate_labels_success(self, monkeypatch):
        """Test successful label validation"""
        # Mock valid labels
        mock_labels = {
            'bot_new_conversation': 'label_1',
            'waiting_urgent_support': 'label_2',
            'waiting_call_before_quote': 'label_3',
            'moving': 'label_4',
            'organization': 'label_5'
        }
        monkeypatch.setattr(whatsapp, 'LABELS', mock_labels)
        
        # Should not raise exception
        ConfigValidator.validate_labels()
        
    def test_validate_labels_missing(self, monkeypatch):
        """Test validation with missing labels"""
        # Mock invalid labels
        mock_labels = {
            'bot_new_conversation': 'label_1',
            'waiting_urgent_support': 'label_2'
            # Missing required labels
        }
        monkeypatch.setattr(whatsapp, 'LABELS', mock_labels)
        
        with pytest.raises(ConfigurationError) as exc:
            ConfigValidator.validate_labels()
        assert "Missing required label" in str(exc.value)
        
    def test_validate_labels_empty(self, monkeypatch):
        """Test validation with empty label IDs"""
        # Mock labels with empty values
        mock_labels = {
            'bot_new_conversation': '',
            'waiting_urgent_support': 'label_2',
            'waiting_call_before_quote': 'label_3',
            'moving': 'label_4',
            'organization': 'label_5'
        }
        monkeypatch.setattr(whatsapp, 'LABELS', mock_labels)
        
        with pytest.raises(ConfigurationError) as exc:
            ConfigValidator.validate_labels()
        assert "invalid/empty IDs" in str(exc.value)
        
    def test_validate_responses_success(self):
        """Test successful response validation"""
        responses = {
            'initial': {'message': 'test'},
            'details_collection': {'message': 'test'},
            'verify_details': {'message': 'test'}
        }
        required_fields = ['initial', 'details_collection', 'verify_details']
        
        # Should not raise exception
        ConfigValidator.validate_responses(responses, required_fields)
        
    def test_validate_responses_missing(self):
        """Test response validation with missing fields"""
        responses = {
            'initial': {'message': 'test'},
            # Missing required fields
        }
        required_fields = ['initial', 'details_collection', 'verify_details']
        
        with pytest.raises(ConfigurationError) as exc:
            ConfigValidator.validate_responses(responses, required_fields)
        assert "Missing required response fields" in str(exc.value)
        
    def test_validate_responses_invalid(self):
        """Test response validation with invalid values"""
        responses = {
            'initial': '',  # Invalid empty string
            'details_collection': None,  # Invalid None
            'verify_details': {'message': 'test'}
        }
        required_fields = ['initial', 'details_collection', 'verify_details']
        
        with pytest.raises(ConfigurationError) as exc:
            ConfigValidator.validate_responses(responses, required_fields)
        assert "Invalid values for response fields" in str(exc.value)
        
    def test_validate_timeouts_success(self):
        """Test successful timeout validation"""
        # Valid timeout values
        ConfigValidator.validate_timeouts(60)  # 1 hour
        ConfigValidator.validate_timeouts(300)  # 5 hours
        
    def test_validate_timeouts_invalid(self):
        """Test timeout validation with invalid values"""
        # Too short
        with pytest.raises(ConfigurationError) as exc:
            ConfigValidator.validate_timeouts(1)
        assert "less than minimum" in str(exc.value)
        
        # Too long
        with pytest.raises(ConfigurationError) as exc:
            ConfigValidator.validate_timeouts(2000)
        assert "exceeds maximum" in str(exc.value)
        
        # Invalid type
        with pytest.raises(ConfigurationError) as exc:
            ConfigValidator.validate_timeouts("60")
        assert "must be an integer" in str(exc.value)
        
    def test_validate_all_success(self, monkeypatch):
        """Test successful validation of all configurations"""
        # Mock valid labels
        mock_labels = {
            'bot_new_conversation': 'label_1',
            'waiting_urgent_support': 'label_2',
            'waiting_call_before_quote': 'label_3',
            'moving': 'label_4',
            'organization': 'label_5'
        }
        monkeypatch.setattr(whatsapp, 'LABELS', mock_labels)
        
        # Should not raise exception
        ConfigValidator.validate_all()
        
    def test_validate_all_failure(self, monkeypatch):
        """Test validation failure of all configurations"""
        # Mock invalid labels
        mock_labels = {
            'bot_new_conversation': '',  # Invalid empty ID
        }
        monkeypatch.setattr(whatsapp, 'LABELS', mock_labels)
        
        with pytest.raises(ConfigurationError) as exc:
            ConfigValidator.validate_all()
        assert "Configuration validation failed" in str(exc.value)