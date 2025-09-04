# 🤝 Contributing to KRSN-RT2I

Thank you for your interest in contributing to KRSN-RT2I! This guide will help you get started with contributing to our advanced real-time threat intelligence platform.

## 🌟 Ways to Contribute

- 🐛 **Bug Reports**: Help us identify and fix issues
- ✨ **Feature Requests**: Suggest new capabilities
- 💻 **Code Contributions**: Submit pull requests
- 📖 **Documentation**: Improve our guides and docs
- 🧪 **Testing**: Help us improve test coverage
- 🔒 **Security**: Report security vulnerabilities
- 🌍 **Translations**: Help make KRSN-RT2I multilingual

## 🚀 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/KRSN-RT2I.git
cd KRSN-RT2I

# Add upstream remote
git remote add upstream https://github.com/STLR-TRAJ/KRSN-RT2I.git
```

### 2. Set Up Development Environment

```bash
# Backend setup
cd backend
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Frontend setup
cd ..
npm install
npm run dev

# Start backend (in separate terminal)
cd backend
python start_server.py
```

### 3. Run Tests

```bash
# Backend tests
cd backend
pytest -v --cov=app

# Frontend tests
npm test

# Integration tests
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

## 📋 Development Guidelines

### 🏗️ Project Structure

```
KRSN-RT2I/
├── 🎨 Frontend (Next.js + TypeScript)
│   ├── app/                # Next.js app directory
│   ├── components/         # React components
│   └── lib/               # Utilities
├── ⚙️ Backend (FastAPI + Python)
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Configuration
│   │   ├── services/      # Business logic
│   │   └── db/            # Database models
├── 🧪 Tests
│   ├── backend/           # Python tests
│   └── frontend/          # Jest/React tests
└── 📚 Documentation
```

### 🎯 Code Style Guidelines

#### Python (Backend)

```python
# Use Black for formatting
black backend/

# Use isort for import sorting
isort backend/

# Use mypy for type checking
mypy backend/

# Follow PEP 8 guidelines
# Use type hints for all functions
def process_threat(indicator: str, threat_type: str) -> ThreatResult:
    """Process a threat indicator and return analysis results."""
    pass

# Use descriptive variable names
threat_score = calculate_threat_score(indicator)
malicious_indicators = filter_malicious(threats)

# Add docstrings to all public functions
def analyze_threat_pattern(patterns: List[str]) -> AnalysisResult:
    """
    Analyze threat patterns using machine learning.
    
    Args:
        patterns: List of threat patterns to analyze
        
    Returns:
        AnalysisResult containing confidence scores and classifications
        
    Raises:
        ValueError: If patterns list is empty
    """
    pass
```

#### TypeScript/React (Frontend)

```typescript
// Use Prettier for formatting
npm run format

// Use ESLint for linting
npm run lint

// Use TypeScript strict mode
interface ThreatData {
  id: string;
  indicator: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  timestamp: Date;
}

// Use React hooks properly
const useThreatData = (threatId: string) => {
  const [threat, setThreat] = useState<ThreatData | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    fetchThreat(threatId).then(setThreat).finally(() => setLoading(false));
  }, [threatId]);
  
  return { threat, loading };
};

// Use proper component naming
export const ThreatAnalysisCard: React.FC<ThreatAnalysisProps> = ({
  threat,
  onAnalyze
}) => {
  return (
    <Card className="threat-analysis">
      {/* Component implementation */}
    </Card>
  );
};
```

### 🗄️ Database Guidelines

```sql
-- Use descriptive table and column names
CREATE TABLE threat_indicators (
    id SERIAL PRIMARY KEY,
    indicator_value VARCHAR(255) NOT NULL,
    indicator_type VARCHAR(50) NOT NULL,
    severity_level VARCHAR(20) NOT NULL,
    confidence_score DECIMAL(3,2),
    first_seen_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add proper indexes
CREATE INDEX idx_threat_indicators_value ON threat_indicators(indicator_value);
CREATE INDEX idx_threat_indicators_type ON threat_indicators(indicator_type);
CREATE INDEX idx_threat_indicators_severity ON threat_indicators(severity_level);

-- Use constraints for data integrity
ALTER TABLE threat_indicators 
ADD CONSTRAINT chk_severity_level 
CHECK (severity_level IN ('critical', 'high', 'medium', 'low'));
```

## 🐛 Bug Reports

### Before Reporting

1. **Search existing issues** to avoid duplicates
2. **Try the latest version** to see if it's already fixed
3. **Check documentation** for known limitations
4. **Reproduce the issue** with minimal steps

### Bug Report Template

```markdown
## 🐛 Bug Description
A clear and concise description of the bug.

## 🔄 Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## ✅ Expected Behavior
What you expected to happen.

## ❌ Actual Behavior
What actually happened.

## 🖼️ Screenshots
If applicable, add screenshots to help explain the problem.

## 🌍 Environment
- OS: [e.g. Windows 11, Ubuntu 22.04]
- Browser: [e.g. Chrome 91, Firefox 89]
- Version: [e.g. 1.2.3]
- Docker: [e.g. 24.0.0]

## 📋 Additional Context
Any other context about the problem.

## 🔍 Logs
```
Paste relevant logs here
```
```

## ✨ Feature Requests

### Feature Request Template

```markdown
## 🚀 Feature Description
A clear and concise description of the feature you'd like to see.

## 🎯 Problem Statement
What problem does this feature solve?

## 💡 Proposed Solution
Describe your proposed solution.

## 🔄 Alternative Solutions
Describe alternatives you've considered.

## 📊 Use Cases
Describe specific use cases for this feature.

## 🎨 Mockups/Examples
Include mockups, examples, or references if applicable.

## 📈 Priority
- [ ] Low
- [ ] Medium
- [ ] High
- [ ] Critical

## 🏷️ Labels
- [ ] enhancement
- [ ] feature
- [ ] ui/ux
- [ ] backend
- [ ] frontend
- [ ] ml/ai
- [ ] security
```

## 💻 Code Contributions

### 🔄 Workflow

1. **Create a branch** for your feature/fix:
   ```bash
   git checkout -b feature/threat-correlation-engine
   # or
   git checkout -b fix/dashboard-loading-issue
   ```

2. **Make your changes** following our guidelines

3. **Write/update tests** for your changes:
   ```bash
   # Backend tests
   pytest tests/test_new_feature.py -v
   
   # Frontend tests
   npm test -- --testPathPattern=NewComponent
   ```

4. **Run quality checks**:
   ```bash
   # Backend
   black backend/
   isort backend/
   mypy backend/
   pytest backend/ --cov=app
   
   # Frontend
   npm run lint:fix
   npm run type-check
   npm test
   ```

5. **Update documentation** if needed

6. **Commit your changes** using conventional commits:
   ```bash
   git commit -m "feat: add advanced threat correlation engine"
   git commit -m "fix: resolve dashboard loading performance issue"
   git commit -m "docs: update API documentation for new endpoints"
   ```

7. **Push to your fork**:
   ```bash
   git push origin feature/threat-correlation-engine
   ```

8. **Create a Pull Request** with detailed description

### 📝 Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

```bash
# Format
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]

# Examples
feat(api): add real-time threat streaming endpoint
fix(dashboard): resolve memory leak in chart components
docs(readme): update installation instructions
test(backend): add integration tests for ML engine
perf(frontend): optimize dashboard rendering performance
refactor(services): restructure threat correlation logic
style(components): apply consistent styling to alerts
chore(deps): update dependencies to latest versions
```

### 🎯 Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding/updating tests
- **perf**: Performance improvements
- **chore**: Build process, dependencies, etc.

### 🔍 Pull Request Guidelines

#### PR Template

```markdown
## 📋 Description
Brief description of changes and motivation.

## 🔗 Related Issues
Closes #123
Related to #456

## 🧪 Type of Change
- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to change)
- [ ] 📖 Documentation update
- [ ] 🎨 Style/UI changes
- [ ] ♻️ Code refactoring
- [ ] ⚡ Performance improvement
- [ ] 🧪 Test addition/update

## ✅ Testing
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] All new and existing tests pass locally
- [ ] I have tested this change in a realistic environment

## 📖 Documentation
- [ ] I have updated the documentation accordingly
- [ ] I have added/updated API documentation if applicable
- [ ] I have updated the README if applicable

## 🔍 Code Quality
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings

## 📸 Screenshots/Videos
If applicable, add screenshots or videos demonstrating the changes.

## 🚀 Deployment Notes
Any special deployment considerations or breaking changes.
```

#### Review Process

1. **Automated Checks**: All PRs must pass:
   - Unit tests
   - Integration tests
   - Code quality checks
   - Security scans

2. **Code Review**: At least one maintainer review required

3. **Documentation**: Updates must include relevant documentation

4. **Testing**: New features require corresponding tests

## 🧪 Testing Guidelines

### Backend Testing

```python
# Unit tests
def test_threat_analysis():
    """Test threat analysis functionality."""
    threat_analyzer = ThreatAnalyzer()
    result = threat_analyzer.analyze("192.168.1.1")
    
    assert result.is_valid
    assert result.score >= 0.0
    assert result.score <= 10.0

# Integration tests
@pytest.mark.integration
def test_api_threat_search():
    """Test threat search API endpoint."""
    response = client.post("/api/v1/threats/search", 
                          json={"query": "test.com"})
    
    assert response.status_code == 200
    assert "results" in response.json()

# Mock external services
@patch('app.services.external_api.AbuseIPDBClient')
def test_external_api_integration(mock_client):
    """Test integration with external threat feeds."""
    mock_client.return_value.check_ip.return_value = {
        "is_malicious": True,
        "confidence": 95
    }
    
    result = check_ip_reputation("1.2.3.4")
    assert result.is_malicious is True
```

### Frontend Testing

```typescript
// Component tests
import { render, screen, fireEvent } from '@testing-library/react';
import { ThreatSearchComponent } from './ThreatSearch';

describe('ThreatSearchComponent', () => {
  test('renders search input and button', () => {
    render(<ThreatSearchComponent />);
    
    expect(screen.getByPlaceholderText('Enter IP, domain, or hash')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Search' })).toBeInTheDocument();
  });

  test('performs search on button click', async () => {
    const mockOnSearch = jest.fn();
    render(<ThreatSearchComponent onSearch={mockOnSearch} />);
    
    const input = screen.getByPlaceholderText('Enter IP, domain, or hash');
    const button = screen.getByRole('button', { name: 'Search' });
    
    fireEvent.change(input, { target: { value: '192.168.1.1' } });
    fireEvent.click(button);
    
    expect(mockOnSearch).toHaveBeenCalledWith('192.168.1.1');
  });
});

// API integration tests
import { API } from '../lib/api';

describe('API Integration', () => {
  test('fetches threat data successfully', async () => {
    const threats = await API.threats.search('test.com');
    
    expect(threats).toHaveProperty('results');
    expect(Array.isArray(threats.results)).toBe(true);
  });
});
```

## 🔒 Security Guidelines

### Reporting Security Vulnerabilities

🚨 **DO NOT** create public issues for security vulnerabilities.

Instead, email us at: **security@krsn-rt2i.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Security Best Practices

```python
# Input validation
from pydantic import BaseModel, validator

class ThreatQuery(BaseModel):
    indicator: str
    
    @validator('indicator')
    def validate_indicator(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Indicator cannot be empty')
        if len(v) > 255:
            raise ValueError('Indicator too long')
        return v.strip()

# SQL injection prevention
from sqlalchemy import text

# ❌ BAD
query = f"SELECT * FROM threats WHERE indicator = '{user_input}'"

# ✅ GOOD
query = text("SELECT * FROM threats WHERE indicator = :indicator")
result = session.execute(query, {"indicator": user_input})

# Authentication
from fastapi import Depends, HTTPException
from app.core.auth import get_current_user

@router.get("/api/v1/threats")
async def get_threats(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=403, detail="User not active")
    return await get_user_threats(current_user.id)
```

## 📖 Documentation Standards

### Code Documentation

```python
def correlate_threats(
    indicators: List[str], 
    correlation_rules: List[CorrelationRule],
    confidence_threshold: float = 0.7
) -> CorrelationResult:
    """
    Correlate multiple threat indicators using specified rules.
    
    This function analyzes relationships between threat indicators
    and identifies potential attack patterns or campaigns.
    
    Args:
        indicators: List of threat indicators to correlate
        correlation_rules: Rules defining how indicators should be correlated
        confidence_threshold: Minimum confidence score for correlations (0.0-1.0)
        
    Returns:
        CorrelationResult containing identified correlations and confidence scores
        
    Raises:
        ValueError: If confidence_threshold is not between 0.0 and 1.0
        CorrelationError: If correlation analysis fails
        
    Example:
        >>> indicators = ["192.168.1.1", "malicious.com", "abc123hash"]
        >>> rules = [IPDomainCorrelationRule(), HashIPCorrelationRule()]
        >>> result = correlate_threats(indicators, rules, 0.8)
        >>> print(f"Found {len(result.correlations)} correlations")
    """
    pass
```

### API Documentation

```python
from fastapi import APIRouter, Query, Path
from typing import Optional

@router.get("/api/v1/threats/{threat_id}")
async def get_threat_details(
    threat_id: str = Path(..., description="Unique threat identifier"),
    include_context: bool = Query(False, description="Include additional context data"),
    format: Optional[str] = Query("json", description="Response format (json, xml)")
) -> ThreatDetailResponse:
    """
    Retrieve detailed information about a specific threat.
    
    This endpoint provides comprehensive information about a threat including:
    - Basic threat metadata
    - Risk assessment scores
    - Source attribution
    - Related indicators
    - Mitigation recommendations
    
    **Example Request:**
    ```
    GET /api/v1/threats/threat_12345?include_context=true
    ```
    
    **Example Response:**
    ```json
    {
        "id": "threat_12345",
        "indicator": "192.168.1.100",
        "type": "ip",
        "severity": "high",
        "score": 8.5,
        "context": {
            "geolocation": {...},
            "reputation": {...}
        }
    }
    ```
    """
    pass
```

## 🎨 UI/UX Guidelines

### Design Principles

1. **Simplicity**: Keep interfaces clean and intuitive
2. **Consistency**: Use established design patterns
3. **Accessibility**: Follow WCAG 2.1 AA guidelines
4. **Performance**: Optimize for fast loading and smooth interactions
5. **Mobile-First**: Design for mobile devices first

### Component Guidelines

```tsx
// Use consistent spacing
const ThreatCard: React.FC<ThreatCardProps> = ({ threat }) => {
  return (
    <Card className="p-6 space-y-4">
      <CardHeader className="pb-2">
        <CardTitle className="text-lg font-semibold">
          {threat.indicator}
        </CardTitle>
        <SeverityBadge severity={threat.severity} />
      </CardHeader>
      
      <CardContent className="space-y-3">
        <ThreatMetrics threat={threat} />
        <ThreatTimeline events={threat.events} />
      </CardContent>
      
      <CardFooter className="pt-4">
        <ThreatActions threat={threat} />
      </CardFooter>
    </Card>
  );
};

// Use semantic HTML
const AlertsSection: React.FC = () => {
  return (
    <section aria-labelledby="alerts-heading">
      <h2 id="alerts-heading" className="sr-only">
        Security Alerts
      </h2>
      <AlertsList />
    </section>
  );
};

// Implement proper loading states
const ThreatSearch: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<ThreatResult[]>([]);
  
  return (
    <div>
      <SearchInput onSearch={handleSearch} disabled={loading} />
      
      {loading ? (
        <div className="flex items-center justify-center p-8">
          <Spinner className="h-8 w-8" />
          <span className="ml-2">Searching threats...</span>
        </div>
      ) : (
        <SearchResults results={results} />
      )}
    </div>
  );
};
```

## 🌍 Internationalization

### Adding Translations

```typescript
// 1. Add translation keys to locale files
// locales/en.json
{
  "threats": {
    "severity": {
      "critical": "Critical",
      "high": "High", 
      "medium": "Medium",
      "low": "Low"
    },
    "search": {
      "placeholder": "Enter IP, domain, or hash",
      "button": "Search",
      "results": "{{count}} threats found"
    }
  }
}

// locales/es.json
{
  "threats": {
    "severity": {
      "critical": "Crítico",
      "high": "Alto",
      "medium": "Medio", 
      "low": "Bajo"
    },
    "search": {
      "placeholder": "Ingrese IP, dominio o hash",
      "button": "Buscar",
      "results": "{{count}} amenazas encontradas"
    }
  }
}

// 2. Use translations in components
import { useTranslation } from 'react-i18next';

const ThreatSearch: React.FC = () => {
  const { t } = useTranslation();
  
  return (
    <div>
      <input 
        placeholder={t('threats.search.placeholder')}
        className="..."
      />
      <button>{t('threats.search.button')}</button>
    </div>
  );
};
```

## 🏆 Recognition

### Contributors Hall of Fame

We recognize outstanding contributions in our:
- 📖 **Documentation**: Contributors page
- 🎖️ **GitHub**: Special contributor badges
- 📢 **Blog**: Featured contributor spotlights
- 🎉 **Events**: Conference speaking opportunities

### Contribution Levels

- **🌟 Contributor**: 1+ merged PR
- **⭐ Regular Contributor**: 5+ merged PRs
- **🌟 Core Contributor**: 15+ merged PRs + consistent involvement
- **🏆 Maintainer**: Trusted community member with write access

## 📞 Getting Help

### 💬 Communication Channels

- **GitHub Discussions**: For general questions and ideas
- **Discord**: Real-time chat with the community
- **Email**: Direct contact with maintainers
- **Stack Overflow**: Tag questions with `krsn-rt2i`

### 📚 Resources

- **Developer Documentation**: `/docs/development/`
- **API Reference**: `/docs/api/`
- **Architecture Guide**: `/docs/architecture/`
- **Troubleshooting**: `/docs/troubleshooting/`

## 📄 License

By contributing to KRSN-RT2I, you agree that your contributions will be licensed under the [MIT License](LICENSE).

---

Thank you for contributing to KRSN-RT2I! Together, we're building the future of threat intelligence for organizations worldwide. 🛡️✨
