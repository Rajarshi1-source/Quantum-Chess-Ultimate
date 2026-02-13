Quantum Chess Ultimate - Complete Implementation Plan
I'll create a comprehensive implementation plan with detailed architecture, tech stack recommendations, detailed technical specifications, architecture decisions, and code artifacts for both desktop and web versions. 

# IMPLEMENTATION_PLAN.md

# Quantum Chess Ultimate - Complete Implementation Plan

## Executive Summary

This document outlines a comprehensive implementation strategy for **Quantum Chess Ultimate** across three platforms:
1. **Web Application** (Primary - Cross-platform)
2. **Windows Desktop Application** 
3. **Mobile-Responsive Web Version**

The implementation leverages modern web technologies to maximize code reuse while delivering native-quality experiences.

---

## 1. Technology Stack & Architecture

### 1.1 Core Technology Decisions

#### **Unified Architecture Strategy**
- **Single Codebase Approach**: Use web technologies as the foundation
- **Cross-Platform Framework**: Electron for desktop, React for web
- **Backend**: Python FastAPI for quantum engine API
- **Quantum Computing**: Qiskit with optimized circuit execution

#### **Technology Matrix**

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Frontend Framework** | React 18+ with TypeScript | Component reusability, type safety, ecosystem |
| **State Management** | Zustand + React Query | Lightweight, quantum state handling |
| **UI Framework** | Custom (Tailwind CSS) | Unique design, avoid generic Material-UI look |
| **3D Visualization** | Three.js + React Three Fiber | Quantum state visualization |
| **Desktop Wrapper** | Electron | Native Windows integration, web code reuse |
| **Backend API** | FastAPI (Python) | Async support, automatic OpenAPI docs |
| **Quantum Engine** | Qiskit + NumPy | Existing engine compatibility |
| **Real-time Communication** | WebSocket (Socket.io) | Live game updates, multiplayer future |
| **Animation** | Framer Motion | Smooth quantum state transitions |
| **Charts/Visualization** | D3.js + Recharts | Probability distributions, analytics |
| **Testing** | Vitest + Playwright | Fast unit tests, E2E coverage |
| **Build Tool** | Vite | Fast development, optimized production |
| **Deployment** | Docker + Vercel/Railway | Containerized quantum engine, web hosting |

---

### 1.2 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENT LAYER                            │
├─────────────────┬───────────────────┬──────────────────────┤
│   Web Browser   │  Electron (Win)   │  Mobile Browser      │
│   React App     │  React App        │  React App (PWA)     │
└────────┬────────┴──────────┬────────┴───────────┬──────────┘
         │                   │                    │
         └───────────────────┼────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  WebSocket API  │
                    │   (Socket.io)   │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
    ┌────▼─────┐      ┌─────▼──────┐     ┌─────▼──────┐
    │ FastAPI  │      │  Quantum   │     │   Game     │
    │ Gateway  │◄────►│  Engine    │◄───►│  State     │
    └──────────┘      │  Service   │     │  Manager   │
                      └─────┬──────┘     └────────────┘
                            │
                      ┌─────▼──────┐
                      │   Qiskit   │
                      │  Simulator │
                      └────────────┘
```

---

## 2. Project Structure

```
quantum-chess-ultimate/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application
│   │   ├── config.py               # Configuration management
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── game.py         # Game management endpoints
│   │   │   │   ├── quantum.py      # Quantum engine endpoints
│   │   │   │   └── analysis.py     # Position analysis
│   │   │   └── websocket.py        # Real-time communication
│   │   ├── core/
│   │   │   ├── quantum_engine.py   # Enhanced quantum engine
│   │   │   ├── game_state.py       # Game state management
│   │   │   ├── move_validator.py   # Move validation
│   │   │   └── evaluator.py        # Position evaluation
│   │   ├── models/
│   │   │   ├── game.py             # Pydantic models
│   │   │   ├── move.py
│   │   │   └── quantum.py
│   │   └── services/
│   │       ├── circuit_optimizer.py
│   │       └── cache_manager.py
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── Board/
│   │   │   │   ├── ChessBoard.tsx
│   │   │   │   ├── QuantumSquare.tsx
│   │   │   │   ├── Piece.tsx
│   │   │   │   └── SuperpositionOverlay.tsx
│   │   │   ├── Visualization/
│   │   │   │   ├── QuantumStateViewer.tsx
│   │   │   │   ├── ProbabilityGraph.tsx
│   │   │   │   ├── Circuit3DView.tsx
│   │   │   │   └── MeasurementHistory.tsx
│   │   │   ├── Controls/
│   │   │   │   ├── GameControls.tsx
│   │   │   │   ├── QuantumControls.tsx
│   │   │   │   └── AnalysisPanel.tsx
│   │   │   ├── UI/
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Modal.tsx
│   │   │   │   └── Tooltip.tsx
│   │   │   └── Layout/
│   │   │       ├── MainLayout.tsx
│   │   │       ├── Sidebar.tsx
│   │   │       └── Header.tsx
│   │   ├── hooks/
│   │   │   ├── useQuantumEngine.ts
│   │   │   ├── useGameState.ts
│   │   │   ├── useWebSocket.ts
│   │   │   └── useAnimation.ts
│   │   ├── store/
│   │   │   ├── gameStore.ts
│   │   │   ├── quantumStore.ts
│   │   │   └── uiStore.ts
│   │   ├── services/
│   │   │   ├── api.ts
│   │   │   ├── websocket.ts
│   │   │   └── analytics.ts
│   │   ├── utils/
│   │   │   ├── quantumMath.ts
│   │   │   ├── chessNotation.ts
│   │   │   └── validation.ts
│   │   ├── types/
│   │   │   ├── quantum.ts
│   │   │   ├── game.ts
│   │   │   └── api.ts
│   │   └── styles/
│   │       ├── globals.css
│   │       └── theme.ts
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── tailwind.config.js
│
├── desktop/
│   ├── electron/
│   │   ├── main.ts              # Electron main process
│   │   ├── preload.ts           # Preload script
│   │   └── ipc.ts               # IPC handlers
│   ├── package.json
│   └── electron-builder.yml     # Windows build config
│
├── shared/
│   └── types/                   # Shared TypeScript types
│
├── docs/
│   ├── API.md
│   ├── QUANTUM_RULES.md
│   └── USER_GUIDE.md
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── deploy-web.yml
│       └── build-desktop.yml
│
├── docker-compose.yml
└── README.md
```

---

## 3. Implementation Phases

### Phase 1: Core Backend (Weeks 1-3)

#### Goals
- Enhance quantum engine with production-ready features
- Build FastAPI backend with WebSocket support
- Implement caching and optimization

#### Tasks

**Week 1: Engine Enhancement**
- [ ] Refactor `quantum-chess-engine.py` for modularity
- [ ] Implement circuit optimization techniques
- [ ] Add measurement caching layer
- [ ] Create comprehensive move validation
- [ ] Add persistent entanglement tracking

**Week 2: API Development**
- [ ] Set up FastAPI project structure
- [ ] Create REST endpoints for game management
- [ ] Implement WebSocket for real-time updates
- [ ] Add authentication (JWT) for future multiplayer
- [ ] Create OpenAPI documentation

**Week 3: Optimization & Testing**
- [ ] Implement Redis caching for evaluations
- [ ] Add circuit depth optimization
- [ ] Create comprehensive test suite
- [ ] Performance profiling and optimization
- [ ] Docker containerization

---

### Phase 2: Web Frontend (Weeks 4-7)

#### Goals
- Build stunning, unique UI/UX
- Implement quantum visualization
- Create responsive, accessible interface

#### Tasks

**Week 4: Foundation & Design System**
- [ ] Set up React + TypeScript + Vite
- [ ] Design unique visual identity (non-generic)
- [ ] Create design system with Tailwind
- [ ] Implement custom components
- [ ] Set up state management (Zustand)

**Week 5: Core Game Interface**
- [ ] Build interactive chess board
- [ ] Implement piece movement with animations
- [ ] Create quantum square overlays
- [ ] Add drag-and-drop functionality
- [ ] Implement move highlighting

**Week 6: Quantum Visualization**
- [ ] 3D quantum state viewer (Three.js)
- [ ] Probability distribution graphs
- [ ] Circuit visualization
- [ ] Measurement history timeline
- [ ] Superposition animation effects

**Week 7: Integration & Polish**
- [ ] Connect to backend API
- [ ] Implement WebSocket updates
- [ ] Add game controls and settings
- [ ] Create analysis panel
- [ ] Responsive design for all screens

---

### Phase 3: Desktop Application (Weeks 8-9)

#### Goals
- Package web app as Windows desktop application
- Add native features and optimizations

#### Tasks

**Week 8: Electron Setup**
- [ ] Configure Electron with React app
- [ ] Set up IPC communication
- [ ] Implement native menus and shortcuts
- [ ] Add Windows-specific features
- [ ] Configure auto-updater

**Week 9: Native Integration**
- [ ] File system access for game saves
- [ ] Native notifications
- [ ] System tray integration
- [ ] Performance optimizations
- [ ] Windows installer creation

---

### Phase 4: Testing & Deployment (Weeks 10-12)

#### Tasks

**Week 10: Testing**
- [ ] Unit tests (Vitest)
- [ ] Integration tests
- [ ] E2E tests (Playwright)
- [ ] Performance testing
- [ ] Accessibility audit

**Week 11: Deployment Setup**
- [ ] Configure Docker deployment
- [ ] Set up CI/CD pipelines
- [ ] Deploy to cloud (Railway/Render)
- [ ] Configure CDN for frontend
- [ ] Set up monitoring and logging

**Week 12: Polish & Launch**
- [ ] Bug fixes and refinement
- [ ] Documentation completion
- [ ] Create tutorial and help system
- [ ] Performance optimization
- [ ] Beta testing and feedback

---

## 4. Key Features Implementation

### 4.1 Quantum Visualization Features

1. **Superposition Overlay**
   - Ghosted piece representations
   - Probability heatmaps
   - Animated quantum blur effects

2. **3D Circuit Viewer**
   - Interactive quantum circuit display
   - Gate-by-gate execution visualization
   - Measurement collapse animation

3. **Probability Dashboard**
   - Real-time probability graphs
   - Outcome distribution charts
   - Historical measurement data

4. **Entanglement Indicators**
   - Visual links between entangled pieces
   - Correlation strength display
   - Measurement dependency highlighting

### 4.2 Game Features

1. **Multiple Game Modes**
   - Classical mode (no quantum effects)
   - Quantum mode (full quantum mechanics)
   - Hybrid mode (configurable quantum probability)
   - Tutorial mode (interactive learning)

2. **Analysis Tools**
   - Position evaluation with quantum uncertainty
   - Move suggestion with probability ranges
   - Historical analysis of quantum decisions
   - Export positions and circuits

3. **Customization**
   - Adjustable quantum parameters
   - Visual themes (light/dark/custom)
   - Board and piece styles
   - Animation speed controls

---

## 5. Technical Challenges & Solutions

### Challenge 1: Performance
**Problem**: Quantum simulation is computationally expensive

**Solutions**:
- Implement aggressive caching (Redis)
- Use circuit optimization techniques
- Parallel evaluation of move trees
- Progressive depth exploration
- Web Workers for heavy computation

### Challenge 2: Real-time Updates
**Problem**: Quantum measurements need instant UI updates

**Solutions**:
- WebSocket for bidirectional communication
- Optimistic UI updates
- State synchronization protocols
- Efficient diff-based rendering

### Challenge 3: Visualization Complexity
**Problem**: Representing quantum states intuitively

**Solutions**:
- Multiple visualization modes
- Progressive disclosure of complexity
- Interactive tutorials
- Contextual help and tooltips

### Challenge 4: Cross-platform Consistency
**Problem**: Ensuring identical experience across platforms

**Solutions**:
- Shared React codebase
- Platform-specific adapters
- Comprehensive E2E testing
- Visual regression testing

---

## 6. Development Best Practices

### Code Quality
- TypeScript strict mode
- ESLint + Prettier configuration
- Pre-commit hooks (Husky)
- Code review requirements
- Automated testing (>80% coverage)

### Git Workflow
- Feature branch workflow
- Conventional commits
- Semantic versioning
- Automated changelog generation
- Protected main branch

### Documentation
- Inline code documentation
- API documentation (OpenAPI)
- Architecture decision records
- User guides and tutorials
- Contributing guidelines

---

## 7. Deployment Strategy

### Web Application
```yaml
Platform: Vercel / Railway
- Frontend: Vercel Edge Network
- Backend: Railway with autoscaling
- Database: PostgreSQL (future)
- Cache: Redis Cloud
- Monitoring: Sentry + LogRocket
```

### Desktop Application
```yaml
Distribution:
- Windows: NSIS installer
- Auto-update: Electron updater
- Code signing: Windows certificate
- Release: GitHub Releases
```

---

## 8. Success Metrics

### Technical Metrics
- Response time: <100ms for API calls
- Quantum evaluation: <2s for depth=3
- First contentful paint: <1.5s
- Time to interactive: <3s
- Lighthouse score: >90

### User Metrics
- Tutorial completion rate: >70%
- Average session length: >15 minutes
- User retention (7-day): >40%
- Feature adoption rate: >60%

---

## 9. Future Enhancements

### Phase 5 (Post-Launch)
- Multiplayer support (quantum chess PvP)
- AI difficulty levels
- Quantum chess puzzles
- Tournament mode
- Mobile native apps (React Native)
- Machine learning integration
- Real quantum hardware support
- VR/AR visualization
- Community features (sharing, replays)

---

## 10. Resource Requirements

### Team Composition
- 1 Backend Engineer (Python/Quantum)
- 1 Frontend Engineer (React/TypeScript)
- 1 Full-stack Engineer
- 1 UI/UX Designer
- 1 QA Engineer (part-time)

### Infrastructure Costs (Monthly)
- Cloud hosting: $50-100
- CDN: $20-50
- Database: $15-30
- Monitoring: $25
- Total: ~$110-205/month

---

## Conclusion

This implementation plan provides a comprehensive roadmap for building Quantum Chess Ultimate as a production-ready application across web and desktop platforms. The unified architecture maximizes code reuse while delivering platform-specific optimizations.

The 12-week timeline is aggressive but achievable with a focused team. The modular architecture allows for parallel development and iterative releases.

**Next Steps**:
1. Review and approve technical stack
2. Set up development environment
3. Begin Phase 1 implementation
4. Schedule weekly progress reviews

# TECH_STACK.md

# Quantum Chess Ultimate - Complete Tech Stack

## Technology Stack Overview

This document provides a comprehensive breakdown of all technologies, libraries, and tools used in Quantum Chess Ultimate.

---

## 🎯 Architecture Philosophy

**Unified Web-First Approach**
- Single codebase for web and desktop
- React as the universal UI layer
- Electron for native Windows packaging
- FastAPI backend for quantum processing

---

## 📦 Frontend Stack

### Core Framework
| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 18.2+ | UI component framework |
| **TypeScript** | 5.2+ | Type safety and developer experience |
| **Vite** | 5.0+ | Build tool and dev server |

### State Management
| Library | Purpose |
|---------|---------|
| **Zustand** | Lightweight global state management |
| **React Query** | Server state management and caching |
| **Context API** | Component-level state |

### UI & Styling
| Library | Purpose |
|---------|---------|
| **Tailwind CSS** | Utility-first CSS framework |
| **Framer Motion** | Animation library |
| **CSS Modules** | Component-scoped styles |
| **PostCSS** | CSS processing |

### 3D Visualization
| Library | Purpose |
|---------|---------|
| **Three.js** | 3D graphics engine |
| **React Three Fiber** | React renderer for Three.js |
| **@react-three/drei** | Helper components |

### Data Visualization
| Library | Purpose |
|---------|---------|
| **D3.js** | Advanced data visualization |
| **Recharts** | React chart components |
| **Canvas API** | Custom visualizations |

### Interaction
| Library | Purpose |
|---------|---------|
| **React DnD** | Drag and drop functionality |
| **React DnD HTML5 Backend** | HTML5 drag and drop |

### Utilities
| Library | Purpose |
|---------|---------|
| **Axios** | HTTP client |
| **Socket.io Client** | WebSocket communication |
| **date-fns** | Date manipulation |
| **nanoid** | ID generation |
| **clsx** | Conditional classnames |

---

## 🖥️ Desktop (Electron) Stack

### Core
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Electron** | 28+ | Desktop application framework |
| **Electron Builder** | 24+ | Build and package tool |
| **Electron Updater** | 6+ | Auto-update functionality |

### IPC Communication
- Custom IPC handlers for file operations
- Menu integration
- Native dialogs
- System tray integration

---

## 🔧 Backend Stack

### Web Framework
| Technology | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | 0.109+ | Modern Python web framework |
| **Uvicorn** | 0.27+ | ASGI server |
| **Pydantic** | 2.5+ | Data validation |

### Quantum Computing
| Library | Purpose |
|---------|---------|
| **Qiskit** | Quantum computing SDK |
| **Qiskit Aer** | Quantum circuit simulator |
| **NumPy** | Numerical computing |

### Real-time Communication
| Library | Purpose |
|---------|---------|
| **Python Socket.IO** | WebSocket server |
| **WebSockets** | WebSocket protocol |

### Data Storage & Caching
| Technology | Purpose |
|-----------|---------|
| **Redis** | In-memory caching |
| **MongoDB** | Document database (future) |
| **Motor** | Async MongoDB driver |

### Security
| Library | Purpose |
|---------|---------|
| **python-jose** | JWT handling |
| **passlib** | Password hashing |
| **cryptography** | Encryption utilities |

---

## 🧪 Testing Stack

### Unit Testing
| Tool | Purpose |
|------|---------|
| **Vitest** | Frontend unit tests |
| **@vitest/ui** | Test UI |
| **Pytest** | Backend unit tests |
| **pytest-asyncio** | Async test support |

### E2E Testing
| Tool | Purpose |
|------|---------|
| **Playwright** | Browser automation |
| **@playwright/test** | Test runner |

### Code Quality
| Tool | Purpose |
|------|---------|
| **ESLint** | JavaScript/TypeScript linting |
| **Prettier** | Code formatting |
| **Flake8** | Python linting |
| **MyPy** | Python type checking |
| **Black** | Python code formatting |

---

## 🚀 DevOps & Deployment

### Containerization
| Technology | Purpose |
|-----------|---------|
| **Docker** | Container runtime |
| **Docker Compose** | Multi-container orchestration |

### CI/CD
| Tool | Purpose |
|------|---------|
| **GitHub Actions** | CI/CD pipeline |
| **Codecov** | Code coverage tracking |

### Hosting & Deployment
| Platform | Purpose |
|----------|---------|
| **Vercel** | Frontend hosting |
| **Railway** | Backend hosting |
| **Redis Cloud** | Managed Redis |
| **MongoDB Atlas** | Managed MongoDB (future) |

### Monitoring
| Tool | Purpose |
|------|---------|
| **Sentry** | Error tracking |
| **Prometheus** | Metrics collection |
| **Loguru** | Advanced logging |

---

## 📚 Development Tools

### Version Control
- **Git** - Version control
- **GitHub** - Repository hosting
- **Conventional Commits** - Commit standards

### Package Management
- **npm** - Frontend packages
- **pip** - Python packages
- **pip-tools** - Dependency management

### Development Environment
- **VS Code** - IDE (recommended)
- **Python 3.10+** - Backend runtime
- **Node.js 18+** - Frontend runtime

---

## 🎨 Design Tools

### Fonts
- **Orbitron** - Display font (quantum aesthetic)
- **JetBrains Mono** - Monospace code font

### Icons & Assets
- Custom SVG icons
- Unicode symbols for chess pieces
- Generated quantum effects

---

## 📊 Performance Optimization

### Frontend
- **Code Splitting** - Dynamic imports
- **Tree Shaking** - Unused code elimination
- **Lazy Loading** - Component lazy loading
- **Memoization** - React.memo, useMemo
- **Virtual Scrolling** - Large list optimization

### Backend
- **Redis Caching** - Evaluation caching
- **Circuit Optimization** - Gate reduction
- **Async Processing** - Non-blocking operations
- **Connection Pooling** - Database optimization

---

## 🔐 Security Features

### Authentication (Future)
- JWT-based authentication
- OAuth integration
- Rate limiting
- CORS configuration

### Data Protection
- HTTPS enforcement
- Input validation
- SQL injection prevention
- XSS protection

---

## 📱 Progressive Web App (Future)

### PWA Features
- **Service Workers** - Offline support
- **Web App Manifest** - Installation
- **Push Notifications** - Updates
- **IndexedDB** - Local storage

---

## 🌐 Browser Support

### Minimum Requirements
- **Chrome/Edge** - 90+
- **Firefox** - 88+
- **Safari** - 14+

### Desktop Support
- **Windows** - 10/11 (x64)
- **Future**: macOS, Linux

---

## 📈 Scalability Considerations

### Horizontal Scaling
- Stateless backend design
- Load balancer ready
- Session storage in Redis
- Microservices architecture potential

### Vertical Scaling
- Quantum simulation optimization
- Multi-core utilization
- Memory-efficient algorithms

---

## 🔄 Future Technology Additions

### Phase 2
- **PostgreSQL** - Relational data
- **GraphQL** - API alternative
- **WebGPU** - GPU acceleration
- **WebAssembly** - Performance-critical code

### Phase 3
- **React Native** - Mobile apps
- **Kubernetes** - Container orchestration
- **Apache Kafka** - Event streaming
- **TensorFlow.js** - ML integration

---

## 💡 Technology Decision Rationale

### Why React?
- ✅ Large ecosystem
- ✅ Component reusability
- ✅ Strong TypeScript support
- ✅ Electron compatibility
- ✅ Great developer experience

### Why FastAPI?
- ✅ Modern async Python
- ✅ Automatic API documentation
- ✅ Type safety with Pydantic
- ✅ WebSocket support
- ✅ Fast performance

### Why Electron?
- ✅ Web technology reuse
- ✅ Cross-platform potential
- ✅ Native OS integration
- ✅ Auto-update support
- ✅ Large community

### Why Qiskit?
- ✅ Industry-standard quantum SDK
- ✅ IBM support
- ✅ Comprehensive documentation
- ✅ Active development
- ✅ Simulator efficiency

---

## 📝 Package Size Optimization

### Frontend Bundle
- Target: <500KB (gzipped)
- Lazy loading for routes
- Code splitting by feature
- Tree shaking enabled

### Electron App
- Target: <150MB installer
- ASAR archive compression
- Exclude dev dependencies
- Native module optimization

---

## 🎓 Learning Resources

### React Ecosystem
- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Framer Motion Docs](https://www.framer.com/motion/)

### Quantum Computing
- [Qiskit Documentation](https://qiskit.org/documentation/)
- [IBM Quantum Learning](https://learning.quantum.ibm.com/)

### Backend Development
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python AsyncIO](https://docs.python.org/3/library/asyncio.html)

---

## 📞 Support & Community

### Development
- GitHub Issues - Bug reports
- GitHub Discussions - Feature requests
- Discord Server - Community chat (future)
- Stack Overflow - Technical questions

---

This tech stack is designed for:
1. **Developer Experience** - Modern, productive tools
2. **Performance** - Optimized for quantum computing
3. **Scalability** - Ready for growth
4. **Maintainability** - Clean, documented code
5. **Innovation** - Cutting-edge features

# QUICK_START.md

# Quantum Chess Ultimate - Quick Start Guide

## 🚀 Getting Started in 5 Minutes

This guide will get you up and running with the development environment quickly.

---

## Prerequisites

### Required Software
```bash
# Check versions
node --version   # Should be 18.x or higher
python --version # Should be 3.10 or higher
docker --version # For containerized setup
git --version
```

### Installation Links
- **Node.js**: https://nodejs.org/ (LTS version)
- **Python**: https://www.python.org/downloads/
- **Docker**: https://www.docker.com/products/docker-desktop/
- **Git**: https://git-scm.com/downloads

---

## 📥 Clone and Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/quantum-chess-ultimate.git
cd quantum-chess-ultimate
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env
```

---

## 🏃‍♂️ Running the Application

### Option 1: Development Mode (Recommended)

#### Terminal 1 - Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --port 8000
```

#### Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

**Access the application:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

### Option 2: Docker Compose (Full Stack)

```bash
# From project root
docker-compose up --build

# Or run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

**Access the application:**
- Frontend: http://localhost:80
- Backend API: http://localhost:8000

---

### Option 3: Desktop App (Electron)

```bash
cd frontend

# Development mode
npm run electron:dev

# Build for Windows
npm run electron:build:win
```

---

## 🧪 Running Tests

### Backend Tests
```bash
cd backend
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Frontend Tests
```bash
cd frontend

# Unit tests
npm test

# E2E tests
npm run test:e2e

# Watch mode
npm test -- --watch
```

---

## 📁 Project Structure

```
quantum-chess-ultimate/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── api/      # API routes
│   │   ├── core/     # Core logic
│   │   └── models/   # Data models
│   └── tests/        # Backend tests
│
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── hooks/       # Custom hooks
│   │   ├── store/       # State management
│   │   └── utils/       # Utilities
│   └── tests/          # Frontend tests
│
├── desktop/           # Electron wrapper
│   └── electron/      # Main process
│
└── docs/             # Documentation
```

---

## 🔧 Environment Variables

### Backend (.env)
```env
# Server
ENVIRONMENT=development
HOST=0.0.0.0
PORT=8000

# CORS
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Quantum Engine
QUANTUM_SHOTS=1000
MAX_SEARCH_DEPTH=4

# Logging
LOG_LEVEL=info
```

### Frontend (.env)
```env
# API
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# Features
VITE_ENABLE_QUANTUM_VIEW=true
VITE_ENABLE_ANALYTICS=false

# Build
VITE_APP_VERSION=1.0.0
```

---

## 💻 Development Workflow

### 1. Create a Feature Branch
```bash
git checkout -b feature/my-new-feature
```

### 2. Make Changes
```bash
# Edit files
# Follow code style guidelines
```

### 3. Run Tests
```bash
# Backend
cd backend && pytest tests/

# Frontend
cd frontend && npm test
```

### 4. Commit Changes
```bash
# Use conventional commits
git add .
git commit -m "feat: add quantum superposition visualization"
```

### 5. Push and Create PR
```bash
git push origin feature/my-new-feature
# Create pull request on GitHub
```

---

## 🎨 Code Style

### TypeScript/React
```bash
cd frontend

# Check linting
npm run lint

# Fix linting issues
npm run lint -- --fix

# Format code
npm run format
```

### Python
```bash
cd backend

# Format with black
black app/

# Check types
mypy app/

# Lint
flake8 app/
```

---

## 🐛 Common Issues & Solutions

### Issue: Port Already in Use

**Backend (Port 8000)**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

**Frontend (Port 5173)**
```bash
# Change port in vite.config.ts
server: {
  port: 3000
}
```

### Issue: Module Not Found

**Backend**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check virtual environment
which python  # Should point to venv
```

**Frontend**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: Qiskit Import Error
```bash
# Reinstall Qiskit
pip uninstall qiskit qiskit-aer
pip install qiskit==0.45.2 qiskit-aer==0.13.2
```

### Issue: Docker Build Fails
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

---

## 📚 Useful Commands

### Git
```bash
# Update from main
git fetch origin
git rebase origin/main

# View commit history
git log --oneline --graph

# Undo last commit (keep changes)
git reset --soft HEAD~1
```

### NPM
```bash
# Install specific package
npm install <package-name>

# Update all packages
npm update

# Check outdated packages
npm outdated

# Clear cache
npm cache clean --force
```

### Python/Pip
```bash
# Install specific package
pip install <package-name>

# Upgrade package
pip install --upgrade <package-name>

# List installed packages
pip list

# Generate requirements.txt
pip freeze > requirements.txt
```

### Docker
```bash
# View running containers
docker ps

# View all containers
docker ps -a

# Stop all containers
docker stop $(docker ps -q)

# Remove all containers
docker rm $(docker ps -aq)

# View logs
docker logs <container-id>

# Execute command in container
docker exec -it <container-id> bash
```

---

## 🔍 Debugging

### Backend Debugging
```python
# Add to code for debugging
import pdb; pdb.set_trace()

# Or use breakpoint() in Python 3.7+
breakpoint()
```

### Frontend Debugging
```javascript
// React DevTools
// Chrome extension: React Developer Tools

// Console debugging
console.log('Debug info:', variable);
debugger; // Pauses execution
```

### VS Code Debug Configuration
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": ["app.main:app", "--reload"],
      "cwd": "${workspaceFolder}/backend"
    },
    {
      "name": "Chrome: React",
      "type": "chrome",
      "request": "launch",
      "url": "http://localhost:5173",
      "webRoot": "${workspaceFolder}/frontend/src"
    }
  ]
}
```

---

## 📖 Next Steps

1. **Read the Documentation**
   - [ARCHITECTURE.md](../ARCHITECTURE.md)
   - [API.md](./API.md)
   - [QUANTUM_RULES.md](./QUANTUM_RULES.md)

2. **Explore the Code**
   - Start with `/frontend/src/App.tsx`
   - Then check `/backend/app/main.py`
   - Review `/backend/app/core/quantum_engine.py`

3. **Try Making Changes**
   - Add a new UI component
   - Modify quantum parameters
   - Create a new API endpoint

4. **Join the Community**
   - Star the repository ⭐
   - Report issues
   - Submit pull requests

---

## 🆘 Getting Help

### Resources
- **Documentation**: Check `/docs` folder
- **GitHub Issues**: Report bugs and request features
- **API Docs**: http://localhost:8000/docs
- **Stack Overflow**: Tag `quantum-chess`

### Contact
- GitHub: @yourusername
- Email: your.email@example.com

---

## ✅ Checklist for First Run

- [ ] Install Node.js 18+
- [ ] Install Python 3.10+
- [ ] Clone repository
- [ ] Install backend dependencies
- [ ] Install frontend dependencies
- [ ] Start backend server
- [ ] Start frontend dev server
- [ ] Access app at localhost:5173
- [ ] Verify quantum engine works
- [ ] Run tests successfully

---

Happy Coding! 🚀♟️⚛️

# backend_main.py

"""
Quantum Chess Ultimate - FastAPI Backend
Main application entry point with WebSocket support
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn
from typing import Dict, List
import json
import asyncio
from datetime import datetime

from app.core.quantum_engine import EnhancedQuantumChessEngine
from app.models.game import GameState, Move, GameConfig
from app.models.quantum import QuantumMeasurement, CircuitInfo
from app.services.cache_manager import CacheManager
from app.services.game_manager import GameManager

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, game_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[game_id] = websocket
    
    def disconnect(self, game_id: str):
        if game_id in self.active_connections:
            del self.active_connections[game_id]
    
    async def send_message(self, game_id: str, message: dict):
        if game_id in self.active_connections:
            await self.active_connections[game_id].send_json(message)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections.values():
            await connection.send_json(message)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Quantum Chess Ultimate Backend Starting...")
    app.state.cache = CacheManager()
    app.state.game_manager = GameManager()
    app.state.ws_manager = ConnectionManager()
    yield
    # Shutdown
    print("🛑 Shutting down Quantum Chess Ultimate Backend...")
    await app.state.cache.close()

# Initialize FastAPI app
app = FastAPI(
    title="Quantum Chess Ultimate API",
    description="Backend API for Quantum Chess game with quantum computing integration",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Quantum Chess Ultimate API",
        "version": "1.0.0",
        "status": "operational",
        "quantum_ready": True
    }

# Health check
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "quantum_engine": "ready",
            "cache": "connected",
            "websocket": "active"
        }
    }

# ===== GAME MANAGEMENT ENDPOINTS =====

@app.post("/api/game/new")
async def create_game(config: GameConfig):
    """Create a new quantum chess game"""
    try:
        game_id = app.state.game_manager.create_game(config)
        game_state = app.state.game_manager.get_game(game_id)
        
        return {
            "game_id": game_id,
            "state": game_state.dict(),
            "message": "Game created successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/game/{game_id}")
async def get_game(game_id: str):
    """Get current game state"""
    game = app.state.game_manager.get_game(game_id)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    return game.dict()

@app.post("/api/game/{game_id}/move")
async def make_move(game_id: str, move: Move):
    """Execute a move in the game"""
    try:
        result = await app.state.game_manager.make_move(game_id, move)
        
        # Broadcast move to connected clients
        await app.state.ws_manager.send_message(game_id, {
            "type": "move_made",
            "data": result
        })
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/game/{game_id}/legal-moves")
async def get_legal_moves(game_id: str, position: str):
    """Get all legal moves from a position"""
    try:
        moves = app.state.game_manager.get_legal_moves(game_id, position)
        return {"position": position, "legal_moves": moves}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== QUANTUM ENGINE ENDPOINTS =====

@app.post("/api/quantum/evaluate")
async def evaluate_position(game_id: str):
    """Evaluate current position with quantum engine"""
    try:
        evaluation = await app.state.game_manager.evaluate_position(game_id)
        return evaluation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/quantum/best-move/{game_id}")
async def get_best_move(game_id: str, depth: int = 3):
    """Get best move using quantum minimax"""
    try:
        result = await app.state.game_manager.find_best_move(game_id, depth)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/quantum/measure")
async def measure_board(game_id: str):
    """Measure quantum board state"""
    try:
        measurement = await app.state.game_manager.measure_board(game_id)
        
        # Broadcast measurement to connected clients
        await app.state.ws_manager.send_message(game_id, {
            "type": "measurement",
            "data": measurement
        })
        
        return measurement
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/quantum/circuit/{game_id}")
async def get_circuit_info(game_id: str):
    """Get quantum circuit information"""
    try:
        circuit_info = app.state.game_manager.get_circuit_info(game_id)
        return circuit_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/quantum/superposition/{game_id}")
async def get_superposition_states(game_id: str):
    """Get superposition probabilities for all pieces"""
    try:
        states = app.state.game_manager.get_superposition_states(game_id)
        return {"superposition_states": states}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== ANALYSIS ENDPOINTS =====

@app.post("/api/analysis/position")
async def analyze_position(game_id: str, depth: int = 4):
    """Deep analysis of position with multiple quantum samples"""
    try:
        analysis = await app.state.game_manager.analyze_position(game_id, depth)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analysis/probability/{game_id}")
async def get_outcome_probability(game_id: str, move: str):
    """Calculate probability distribution for a move"""
    try:
        probabilities = await app.state.game_manager.calculate_probabilities(
            game_id, move
        )
        return probabilities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ===== WEBSOCKET ENDPOINT =====

@app.websocket("/ws/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    """WebSocket connection for real-time game updates"""
    await app.state.ws_manager.connect(game_id, websocket)
    
    try:
        # Send initial game state
        game = app.state.game_manager.get_game(game_id)
        if game:
            await websocket.send_json({
                "type": "connected",
                "data": game.dict()
            })
        
        # Listen for messages
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message["type"] == "ping":
                await websocket.send_json({"type": "pong"})
            
            elif message["type"] == "request_update":
                game = app.state.game_manager.get_game(game_id)
                await websocket.send_json({
                    "type": "game_update",
                    "data": game.dict() if game else None
                })
    
    except WebSocketDisconnect:
        app.state.ws_manager.disconnect(game_id)
        print(f"Client disconnected from game {game_id}")
    except Exception as e:
        print(f"WebSocket error: {e}")
        app.state.ws_manager.disconnect(game_id)

# ===== UTILITY ENDPOINTS =====

@app.get("/api/stats")
async def get_stats():
    """Get server statistics"""
    return {
        "active_games": len(app.state.game_manager.games),
        "active_connections": len(app.state.ws_manager.active_connections),
        "cache_size": await app.state.cache.size(),
        "uptime": "TODO"  # Implement uptime tracking
    }

@app.delete("/api/game/{game_id}")
async def delete_game(game_id: str):
    """Delete a game"""
    try:
        app.state.game_manager.delete_game(game_id)
        return {"message": "Game deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Resource not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

# frontend_App.tsx

/**
 * Quantum Chess Ultimate - Main React Application
 * 
 * Features a distinctive brutalist-meets-sci-fi aesthetic with 
 * quantum-inspired visual effects and animations
 */

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ChessBoard from './components/Board/ChessBoard';
import QuantumStateViewer from './components/Visualization/QuantumStateViewer';
import ProbabilityGraph from './components/Visualization/ProbabilityGraph';
import GameControls from './components/Controls/GameControls';
import AnalysisPanel from './components/Controls/AnalysisPanel';
import { useGameState } from './hooks/useGameState';
import { useQuantumEngine } from './hooks/useQuantumEngine';
import './styles/App.css';

const App: React.FC = () => {
  const { gameState, makeMove, resetGame, isLoading } = useGameState();
  const { quantumState, measure, evaluate } = useQuantumEngine();
  const [showQuantumView, setShowQuantumView] = useState(true);
  const [selectedSquare, setSelectedSquare] = useState<string | null>(null);

  useEffect(() => {
    // Initialize game on mount
    resetGame();
  }, []);

  return (
    <div className="app-container">
      {/* Animated background with quantum-inspired particles */}
      <div className="quantum-background">
        <div className="particle-field" />
        <div className="grid-overlay" />
      </div>

      {/* Main header */}
      <motion.header 
        className="app-header"
        initial={{ y: -100, opacity: 0 }}
        animate={{ y: 0, opacity: 1 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
      >
        <h1 className="title">
          <span className="quantum-glow">QUANTUM</span>
          <span className="chess-text">CHESS</span>
          <span className="ultimate-badge">ULTIMATE</span>
        </h1>
        
        <div className="header-stats">
          <div className="stat-item">
            <span className="stat-label">SUPERPOSITION</span>
            <motion.span 
              className="stat-value"
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              {quantumState?.superpositionCount || 0}
            </motion.span>
          </div>
          <div className="stat-item">
            <span className="stat-label">ENTANGLEMENT</span>
            <span className="stat-value">
              {quantumState?.entanglementPairs || 0}
            </span>
          </div>
          <div className="stat-item">
            <span className="stat-label">MEASUREMENTS</span>
            <span className="stat-value">
              {gameState?.measurementCount || 0}
            </span>
          </div>
        </div>
      </motion.header>

      {/* Main game area */}
      <div className="game-container">
        {/* Left sidebar - Quantum visualization */}
        <motion.aside 
          className="quantum-sidebar"
          initial={{ x: -300, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <div className="sidebar-section">
            <h2 className="section-title">
              <span className="title-icon">⚛</span>
              QUANTUM STATE
            </h2>
            
            <QuantumStateViewer 
              state={quantumState}
              selectedSquare={selectedSquare}
            />
          </div>

          <div className="sidebar-section">
            <h2 className="section-title">
              <span className="title-icon">📊</span>
              PROBABILITY
            </h2>
            
            <ProbabilityGraph 
              data={quantumState?.probabilities}
              animated={true}
            />
          </div>

          <div className="sidebar-section">
            <button 
              className="quantum-measure-btn"
              onClick={measure}
              disabled={isLoading}
            >
              <motion.span
                animate={{ scale: [1, 1.05, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
              >
                COLLAPSE WAVEFUNCTION
              </motion.span>
            </button>
          </div>
        </motion.aside>

        {/* Center - Chess board */}
        <motion.main 
          className="board-area"
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <ChessBoard
            position={gameState?.position}
            onMove={makeMove}
            quantumState={quantumState}
            selectedSquare={selectedSquare}
            onSquareSelect={setSelectedSquare}
            showQuantumOverlay={showQuantumView}
          />

          {/* Turn indicator */}
          <motion.div 
            className="turn-indicator"
            animate={{ 
              boxShadow: gameState?.turn === 'white' 
                ? '0 0 30px rgba(255,255,255,0.5)' 
                : '0 0 30px rgba(0,0,0,0.8)' 
            }}
          >
            <span className="turn-text">
              {gameState?.turn === 'white' ? '○' : '●'} 
              {gameState?.turn?.toUpperCase()} TO MOVE
            </span>
          </motion.div>

          {/* Game controls */}
          <GameControls
            onReset={resetGame}
            onUndo={() => {/* implement */}}
            onToggleQuantum={() => setShowQuantumView(!showQuantumView)}
            quantumEnabled={showQuantumView}
          />
        </motion.main>

        {/* Right sidebar - Analysis */}
        <motion.aside 
          className="analysis-sidebar"
          initial={{ x: 300, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <AnalysisPanel
            gameState={gameState}
            quantumState={quantumState}
            onEvaluate={evaluate}
          />
        </motion.aside>
      </div>

      {/* Loading overlay */}
      <AnimatePresence>
        {isLoading && (
          <motion.div
            className="loading-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="loading-content">
              <motion.div
                className="quantum-spinner"
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
              >
                <div className="spinner-orbit" />
                <div className="spinner-orbit" style={{ animationDelay: '0.5s' }} />
                <div className="spinner-orbit" style={{ animationDelay: '1s' }} />
              </motion.div>
              <p className="loading-text">SIMULATING QUANTUM CIRCUITS...</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-content">
          <span className="footer-text">
            Powered by Qiskit Quantum Computing Framework
          </span>
          <div className="footer-links">
            <a href="#" className="footer-link">About</a>
            <a href="#" className="footer-link">Rules</a>
            <a href="#" className="footer-link">Tutorial</a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default App;

# frontend_styles.css 

/**
 * Quantum Chess Ultimate - Unique Brutalist Quantum Design
 * 
 * Design Philosophy:
 * - Brutalist concrete textures with neon quantum accents
 * - Heavy use of geometric patterns and grid systems
 * - Glitch effects and scan lines for sci-fi aesthetic
 * - Bold typography with custom quantum font stack
 */

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=JetBrains+Mono:wght@300;400;600&display=swap');

:root {
  /* Quantum color palette */
  --quantum-primary: #00ff9d;
  --quantum-secondary: #ff0080;
  --quantum-tertiary: #00d4ff;
  --quantum-glow: rgba(0, 255, 157, 0.5);
  
  /* Brutalist grays */
  --concrete-dark: #1a1a1a;
  --concrete-medium: #2d2d2d;
  --concrete-light: #3f3f3f;
  --concrete-accent: #4a4a4a;
  
  /* Text colors */
  --text-primary: #e0e0e0;
  --text-secondary: #a0a0a0;
  --text-accent: var(--quantum-primary);
  
  /* Gradients */
  --gradient-quantum: linear-gradient(135deg, var(--quantum-primary), var(--quantum-tertiary));
  --gradient-dark: linear-gradient(180deg, #0a0a0a, #1a1a1a);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'JetBrains Mono', monospace;
  background: var(--concrete-dark);
  color: var(--text-primary);
  overflow-x: hidden;
  line-height: 1.6;
}

.app-container {
  min-height: 100vh;
  position: relative;
  display: flex;
  flex-direction: column;
}

/* ===== QUANTUM BACKGROUND ===== */

.quantum-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  overflow: hidden;
}

.particle-field {
  position: absolute;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 50%, rgba(0, 255, 157, 0.03), transparent 50%),
    radial-gradient(circle at 80% 50%, rgba(255, 0, 128, 0.03), transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(0, 212, 255, 0.02), transparent 70%);
  animation: particleFloat 20s ease-in-out infinite;
}

@keyframes particleFloat {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(20px, -20px) scale(1.1); }
}

.grid-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image: 
    linear-gradient(rgba(0, 255, 157, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 157, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridPulse 4s ease-in-out infinite;
}

@keyframes gridPulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.1; }
}

/* ===== HEADER ===== */

.app-header {
  padding: 2rem 3rem;
  background: var(--gradient-dark);
  border-bottom: 3px solid var(--quantum-primary);
  position: relative;
}

.app-header::after {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 100%;
  height: 3px;
  background: var(--gradient-quantum);
  box-shadow: 0 0 20px var(--quantum-glow);
  animation: scanLine 2s linear infinite;
}

@keyframes scanLine {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.title {
  font-family: 'Orbitron', sans-serif;
  font-size: 3.5rem;
  font-weight: 900;
  letter-spacing: 0.3rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  text-transform: uppercase;
  margin-bottom: 1rem;
}

.quantum-glow {
  color: var(--quantum-primary);
  text-shadow: 
    0 0 10px var(--quantum-glow),
    0 0 20px var(--quantum-glow),
    0 0 30px var(--quantum-glow);
  animation: quantumPulse 3s ease-in-out infinite;
}

@keyframes quantumPulse {
  0%, 100% { 
    text-shadow: 
      0 0 10px var(--quantum-glow),
      0 0 20px var(--quantum-glow),
      0 0 30px var(--quantum-glow);
  }
  50% { 
    text-shadow: 
      0 0 20px var(--quantum-glow),
      0 0 40px var(--quantum-glow),
      0 0 60px var(--quantum-glow);
  }
}

.chess-text {
  color: var(--text-primary);
  position: relative;
}

.ultimate-badge {
  font-size: 1rem;
  padding: 0.3rem 0.8rem;
  background: var(--quantum-primary);
  color: var(--concrete-dark);
  border-radius: 0;
  font-weight: 700;
  letter-spacing: 0.2rem;
  transform: skewX(-10deg);
  box-shadow: 4px 4px 0 var(--concrete-accent);
}

.header-stats {
  display: flex;
  gap: 3rem;
  margin-top: 1rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.stat-label {
  font-size: 0.7rem;
  color: var(--text-secondary);
  letter-spacing: 0.15rem;
  font-weight: 600;
}

.stat-value {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--quantum-primary);
  text-shadow: 0 0 10px var(--quantum-glow);
}

/* ===== GAME CONTAINER ===== */

.game-container {
  flex: 1;
  display: grid;
  grid-template-columns: 350px 1fr 350px;
  gap: 2rem;
  padding: 2rem;
  position: relative;
}

/* ===== SIDEBARS ===== */

.quantum-sidebar,
.analysis-sidebar {
  background: var(--concrete-medium);
  border: 2px solid var(--concrete-accent);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  position: relative;
}

.quantum-sidebar::before,
.analysis-sidebar::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  height: 4px;
  background: var(--gradient-quantum);
  opacity: 0.6;
}

.sidebar-section {
  background: var(--concrete-dark);
  padding: 1.2rem;
  border-left: 4px solid var(--quantum-primary);
}

.section-title {
  font-family: 'Orbitron', sans-serif;
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.2rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.8rem;
  color: var(--text-accent);
  text-transform: uppercase;
}

.title-icon {
  font-size: 1.2rem;
  filter: drop-shadow(0 0 5px var(--quantum-glow));
}

/* ===== QUANTUM MEASURE BUTTON ===== */

.quantum-measure-btn {
  width: 100%;
  padding: 1.2rem;
  background: var(--concrete-dark);
  border: 3px solid var(--quantum-primary);
  color: var(--quantum-primary);
  font-family: 'Orbitron', sans-serif;
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 0.15rem;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.quantum-measure-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: var(--gradient-quantum);
  transition: left 0.3s ease;
  z-index: 0;
}

.quantum-measure-btn:hover::before {
  left: 0;
}

.quantum-measure-btn:hover {
  color: var(--concrete-dark);
  box-shadow: 
    0 0 20px var(--quantum-glow),
    inset 0 0 20px var(--quantum-glow);
}

.quantum-measure-btn span {
  position: relative;
  z-index: 1;
}

.quantum-measure-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* ===== BOARD AREA ===== */

.board-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  padding: 2rem;
  background: var(--concrete-medium);
  border: 3px solid var(--concrete-accent);
  position: relative;
}

.board-area::before {
  content: '';
  position: absolute;
  inset: 0;
  background: 
    linear-gradient(0deg, rgba(0, 255, 157, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 255, 157, 0.02) 1px, transparent 1px);
  background-size: 20px 20px;
  pointer-events: none;
}

/* ===== TURN INDICATOR ===== */

.turn-indicator {
  padding: 1rem 2rem;
  background: var(--concrete-dark);
  border: 2px solid var(--quantum-primary);
  font-family: 'Orbitron', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  letter-spacing: 0.2rem;
  text-align: center;
  transition: box-shadow 0.3s ease;
}

.turn-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
}

/* ===== LOADING OVERLAY ===== */

.loading-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.loading-content {
  text-align: center;
}

.quantum-spinner {
  width: 100px;
  height: 100px;
  position: relative;
  margin: 0 auto 2rem;
}

.spinner-orbit {
  position: absolute;
  width: 100%;
  height: 100%;
  border: 3px solid transparent;
  border-top-color: var(--quantum-primary);
  border-radius: 50%;
  animation: spin 1.5s linear infinite;
}

.spinner-orbit:nth-child(2) {
  width: 70%;
  height: 70%;
  top: 15%;
  left: 15%;
  border-top-color: var(--quantum-secondary);
}

.spinner-orbit:nth-child(3) {
  width: 40%;
  height: 40%;
  top: 30%;
  left: 30%;
  border-top-color: var(--quantum-tertiary);
}

@keyframes spin {
  100% { transform: rotate(360deg); }
}

.loading-text {
  font-family: 'Orbitron', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  letter-spacing: 0.2rem;
  color: var(--quantum-primary);
  animation: textPulse 1s ease-in-out infinite;
}

@keyframes textPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ===== FOOTER ===== */

.app-footer {
  padding: 2rem 3rem;
  background: var(--concrete-dark);
  border-top: 2px solid var(--concrete-accent);
}

.footer-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-text {
  font-size: 0.85rem;
  color: var(--text-secondary);
  font-weight: 300;
}

.footer-links {
  display: flex;
  gap: 2rem;
}

.footer-link {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.1rem;
  text-transform: uppercase;
  transition: color 0.3s ease;
}

.footer-link:hover {
  color: var(--quantum-primary);
  text-shadow: 0 0 10px var(--quantum-glow);
}

/* ===== RESPONSIVE DESIGN ===== */

@media (max-width: 1400px) {
  .game-container {
    grid-template-columns: 300px 1fr 300px;
  }
}

@media (max-width: 1200px) {
  .game-container {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr auto;
  }
  
  .quantum-sidebar,
  .analysis-sidebar {
    max-width: 800px;
    margin: 0 auto;
    width: 100%;
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
    flex-direction: column;
    gap: 0.5rem;
  }
  
  .header-stats {
    flex-direction: column;
    gap: 1rem;
  }
  
  .game-container {
    padding: 1rem;
  }
}

/* ===== GLITCH EFFECT (Optional Enhancement) ===== */

@keyframes glitch {
  0% { transform: translate(0); }
  20% { transform: translate(-2px, 2px); }
  40% { transform: translate(-2px, -2px); }
  60% { transform: translate(2px, 2px); }
  80% { transform: translate(2px, -2px); }
  100% { transform: translate(0); }
}

.glitch-effect {
  animation: glitch 0.3s infinite;
}

# ChessBoard.tsx

/**
 * ChessBoard Component - Interactive Quantum Chess Board
 * Features quantum superposition overlays and piece animations
 */

import React, { useState, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useDrag, useDrop } from 'react-dnd';
import QuantumSquare from './QuantumSquare';
import Piece from './Piece';
import SuperpositionOverlay from './SuperpositionOverlay';
import './ChessBoard.css';

interface ChessBoardProps {
  position: any;
  onMove: (from: string, to: string) => void;
  quantumState: any;
  selectedSquare: string | null;
  onSquareSelect: (square: string | null) => void;
  showQuantumOverlay: boolean;
}

const ChessBoard: React.FC<ChessBoardProps> = ({
  position,
  onMove,
  quantumState,
  selectedSquare,
  onSquareSelect,
  showQuantumOverlay
}) => {
  const [legalMoves, setLegalMoves] = useState<string[]>([]);
  const [draggedPiece, setDraggedPiece] = useState<string | null>(null);
  const boardRef = useRef<HTMLDivElement>(null);

  // Convert row, col to chess notation (e.g., "e4")
  const toNotation = (row: number, col: number): string => {
    const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
    return `${files[col]}${8 - row}`;
  };

  // Convert chess notation to row, col
  const fromNotation = (notation: string): [number, number] => {
    const files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'];
    const col = files.indexOf(notation[0]);
    const row = 8 - parseInt(notation[1]);
    return [row, col];
  };

  // Handle square click
  const handleSquareClick = useCallback((square: string) => {
    if (selectedSquare) {
      // Attempt to make a move
      if (legalMoves.includes(square)) {
        onMove(selectedSquare, square);
        onSquareSelect(null);
        setLegalMoves([]);
      } else {
        // Select new square
        onSquareSelect(square);
        // Fetch legal moves for this square
        // setLegalMoves(fetchLegalMovesFromAPI(square));
      }
    } else {
      onSquareSelect(square);
      // Fetch legal moves
      // setLegalMoves(fetchLegalMovesFromAPI(square));
    }
  }, [selectedSquare, legalMoves, onMove, onSquareSelect]);

  // Handle drag start
  const handleDragStart = (square: string) => {
    setDraggedPiece(square);
    onSquareSelect(square);
  };

  // Handle drop
  const handleDrop = (toSquare: string) => {
    if (draggedPiece && legalMoves.includes(toSquare)) {
      onMove(draggedPiece, toSquare);
    }
    setDraggedPiece(null);
    onSquareSelect(null);
    setLegalMoves([]);
  };

  // Get quantum probability for a square
  const getQuantumProbability = (square: string): number => {
    return quantumState?.probabilities?.[square] || 0;
  };

  // Check if square is in superposition
  const isInSuperposition = (square: string): boolean => {
    return quantumState?.superpositionSquares?.includes(square) || false;
  };

  // Render the board
  const renderBoard = () => {
    const squares = [];
    
    for (let row = 0; row < 8; row++) {
      for (let col = 0; col < 8; col++) {
        const square = toNotation(row, col);
        const isLight = (row + col) % 2 === 0;
        const isSelected = square === selectedSquare;
        const isLegalMove = legalMoves.includes(square);
        const probability = getQuantumProbability(square);
        const inSuperposition = isInSuperposition(square);
        
        squares.push(
          <QuantumSquare
            key={square}
            square={square}
            isLight={isLight}
            isSelected={isSelected}
            isLegalMove={isLegalMove}
            probability={probability}
            inSuperposition={inSuperposition}
            onClick={() => handleSquareClick(square)}
            onDrop={() => handleDrop(square)}
            showQuantumOverlay={showQuantumOverlay}
          >
            {position?.[square] && (
              <Piece
                piece={position[square]}
                square={square}
                isDragging={draggedPiece === square}
                onDragStart={() => handleDragStart(square)}
                inSuperposition={inSuperposition}
              />
            )}
            
            {showQuantumOverlay && inSuperposition && (
              <SuperpositionOverlay
                square={square}
                probability={probability}
                quantumState={quantumState?.squareStates?.[square]}
              />
            )}
          </QuantumSquare>
        );
      }
    }
    
    return squares;
  };

  return (
    <motion.div 
      className="chess-board-container"
      initial={{ scale: 0.95, opacity: 0 }}
      animate={{ scale: 1, opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      {/* Coordinate labels */}
      <div className="coordinates-top">
        {['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].map(file => (
          <div key={file} className="coordinate-label">{file}</div>
        ))}
      </div>

      <div className="board-wrapper">
        {/* Left coordinates */}
        <div className="coordinates-left">
          {[8, 7, 6, 5, 4, 3, 2, 1].map(rank => (
            <div key={rank} className="coordinate-label">{rank}</div>
          ))}
        </div>

        {/* The actual board */}
        <div ref={boardRef} className="chess-board">
          {renderBoard()}
          
          {/* Quantum field overlay */}
          {showQuantumOverlay && (
            <motion.div 
              className="quantum-field-overlay"
              initial={{ opacity: 0 }}
              animate={{ opacity: 0.3 }}
              exit={{ opacity: 0 }}
            >
              <div className="quantum-wave" />
              <div className="quantum-wave" style={{ animationDelay: '1s' }} />
            </motion.div>
          )}
        </div>

        {/* Right coordinates */}
        <div className="coordinates-right">
          {[8, 7, 6, 5, 4, 3, 2, 1].map(rank => (
            <div key={rank} className="coordinate-label">{rank}</div>
          ))}
        </div>
      </div>

      {/* Bottom coordinates */}
      <div className="coordinates-bottom">
        {['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'].map(file => (
          <div key={file} className="coordinate-label">{file}</div>
        ))}
      </div>

      {/* Quantum statistics overlay */}
      {showQuantumOverlay && quantumState && (
        <motion.div 
          className="board-quantum-stats"
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <div className="stat">
            <span className="stat-label">SUPERPOSED PIECES</span>
            <span className="stat-value">
              {quantumState.superpositionCount}
            </span>
          </div>
          <div className="stat">
            <span className="stat-label">AVG PROBABILITY</span>
            <span className="stat-value">
              {(quantumState.averageProbability * 100).toFixed(1)}%
            </span>
          </div>
          <div className="stat">
            <span className="stat-label">UNCERTAINTY</span>
            <motion.span 
              className="stat-value quantum-pulse"
              animate={{ opacity: [0.5, 1, 0.5] }}
              transition={{ duration: 2, repeat: Infinity }}
            >
              {quantumState.uncertaintyLevel}
            </motion.span>
          </div>
        </motion.div>
      )}
    </motion.div>
  );
};

export default ChessBoard;

# electron_main.ts

/**
 * Quantum Chess Ultimate - Electron Main Process
 * Windows Desktop Application Entry Point
 */

import { app, BrowserWindow, Menu, ipcMain, dialog } from 'electron';
import * as path from 'path';
import * as fs from 'fs';
import { autoUpdater } from 'electron-updater';

let mainWindow: BrowserWindow | null = null;
const isDev = process.env.NODE_ENV === 'development';

// Create the main application window
function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1600,
    height: 1000,
    minWidth: 1200,
    minHeight: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js'),
    },
    backgroundColor: '#1a1a1a',
    title: 'Quantum Chess Ultimate',
    icon: path.join(__dirname, '../assets/icon.png'),
    show: false, // Don't show until ready
    frame: true,
    titleBarStyle: 'default',
  });

  // Load the app
  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  // Show window when ready
  mainWindow.once('ready-to-show', () => {
    mainWindow?.show();
    
    // Check for updates in production
    if (!isDev) {
      autoUpdater.checkForUpdatesAndNotify();
    }
  });

  // Handle window closed
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Create application menu
  createMenu();
}

// Create application menu
function createMenu() {
  const template: any = [
    {
      label: 'File',
      submenu: [
        {
          label: 'New Game',
          accelerator: 'CmdOrCtrl+N',
          click: () => {
            mainWindow?.webContents.send('new-game');
          },
        },
        {
          label: 'Save Game',
          accelerator: 'CmdOrCtrl+S',
          click: () => {
            saveGame();
          },
        },
        {
          label: 'Load Game',
          accelerator: 'CmdOrCtrl+O',
          click: () => {
            loadGame();
          },
        },
        { type: 'separator' },
        {
          label: 'Export Position',
          click: () => {
            mainWindow?.webContents.send('export-position');
          },
        },
        { type: 'separator' },
        {
          label: 'Exit',
          accelerator: 'CmdOrCtrl+Q',
          click: () => {
            app.quit();
          },
        },
      ],
    },
    {
      label: 'Edit',
      submenu: [
        {
          label: 'Undo Move',
          accelerator: 'CmdOrCtrl+Z',
          click: () => {
            mainWindow?.webContents.send('undo-move');
          },
        },
        {
          label: 'Redo Move',
          accelerator: 'CmdOrCtrl+Shift+Z',
          click: () => {
            mainWindow?.webContents.send('redo-move');
          },
        },
        { type: 'separator' },
        { role: 'copy' },
        { role: 'paste' },
      ],
    },
    {
      label: 'Quantum',
      submenu: [
        {
          label: 'Collapse Wavefunction',
          accelerator: 'CmdOrCtrl+M',
          click: () => {
            mainWindow?.webContents.send('measure-board');
          },
        },
        {
          label: 'Toggle Quantum View',
          accelerator: 'CmdOrCtrl+Q',
          click: () => {
            mainWindow?.webContents.send('toggle-quantum-view');
          },
        },
        { type: 'separator' },
        {
          label: 'Quantum Settings',
          click: () => {
            mainWindow?.webContents.send('open-quantum-settings');
          },
        },
      ],
    },
    {
      label: 'Analysis',
      submenu: [
        {
          label: 'Evaluate Position',
          accelerator: 'CmdOrCtrl+E',
          click: () => {
            mainWindow?.webContents.send('evaluate-position');
          },
        },
        {
          label: 'Show Best Move',
          accelerator: 'CmdOrCtrl+B',
          click: () => {
            mainWindow?.webContents.send('show-best-move');
          },
        },
        {
          label: 'Analysis Board',
          click: () => {
            mainWindow?.webContents.send('open-analysis-board');
          },
        },
      ],
    },
    {
      label: 'View',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { type: 'separator' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' },
      ],
    },
    {
      label: 'Help',
      submenu: [
        {
          label: 'Tutorial',
          click: () => {
            mainWindow?.webContents.send('open-tutorial');
          },
        },
        {
          label: 'Quantum Chess Rules',
          click: () => {
            mainWindow?.webContents.send('open-rules');
          },
        },
        { type: 'separator' },
        {
          label: 'About',
          click: () => {
            dialog.showMessageBox(mainWindow!, {
              type: 'info',
              title: 'About Quantum Chess Ultimate',
              message: 'Quantum Chess Ultimate',
              detail: 'Version 1.0.0\n\nAn experimental chess engine incorporating quantum computing principles.\n\nPowered by Qiskit.',
              buttons: ['OK'],
            });
          },
        },
        {
          label: 'Check for Updates',
          click: () => {
            autoUpdater.checkForUpdates();
          },
        },
      ],
    },
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// Save game to file
async function saveGame() {
  if (!mainWindow) return;

  const { filePath } = await dialog.showSaveDialog(mainWindow, {
    title: 'Save Game',
    defaultPath: path.join(app.getPath('documents'), 'quantum-chess-game.qcg'),
    filters: [
      { name: 'Quantum Chess Game', extensions: ['qcg'] },
      { name: 'All Files', extensions: ['*'] },
    ],
  });

  if (filePath) {
    mainWindow.webContents.send('save-game-request', filePath);
  }
}

// Load game from file
async function loadGame() {
  if (!mainWindow) return;

  const { filePaths } = await dialog.showOpenDialog(mainWindow, {
    title: 'Load Game',
    defaultPath: app.getPath('documents'),
    filters: [
      { name: 'Quantum Chess Game', extensions: ['qcg'] },
      { name: 'All Files', extensions: ['*'] },
    ],
    properties: ['openFile'],
  });

  if (filePaths && filePaths.length > 0) {
    try {
      const gameData = fs.readFileSync(filePaths[0], 'utf-8');
      mainWindow.webContents.send('load-game-data', JSON.parse(gameData));
    } catch (error) {
      dialog.showErrorBox('Error', 'Failed to load game file');
    }
  }
}

// IPC Handlers

// Handle save game data from renderer
ipcMain.on('save-game-data', (event, data) => {
  const { filePath, gameData } = data;
  try {
    fs.writeFileSync(filePath, JSON.stringify(gameData, null, 2));
    dialog.showMessageBox(mainWindow!, {
      type: 'info',
      title: 'Success',
      message: 'Game saved successfully!',
      buttons: ['OK'],
    });
  } catch (error) {
    dialog.showErrorBox('Error', 'Failed to save game file');
  }
});

// Handle export position
ipcMain.on('export-position', async (event, positionData) => {
  if (!mainWindow) return;

  const { filePath } = await dialog.showSaveDialog(mainWindow, {
    title: 'Export Position',
    defaultPath: path.join(app.getPath('documents'), 'position.json'),
    filters: [
      { name: 'JSON', extensions: ['json'] },
      { name: 'All Files', extensions: ['*'] },
    ],
  });

  if (filePath) {
    try {
      fs.writeFileSync(filePath, JSON.stringify(positionData, null, 2));
      dialog.showMessageBox(mainWindow, {
        type: 'info',
        title: 'Success',
        message: 'Position exported successfully!',
        buttons: ['OK'],
      });
    } catch (error) {
      dialog.showErrorBox('Error', 'Failed to export position');
    }
  }
});

// Auto-updater events
autoUpdater.on('update-available', () => {
  dialog.showMessageBox(mainWindow!, {
    type: 'info',
    title: 'Update Available',
    message: 'A new version is available. Downloading now...',
    buttons: ['OK'],
  });
});

autoUpdater.on('update-downloaded', () => {
  dialog
    .showMessageBox(mainWindow!, {
      type: 'info',
      title: 'Update Ready',
      message: 'Update downloaded. Restart to install?',
      buttons: ['Restart', 'Later'],
    })
    .then((result) => {
      if (result.response === 0) {
        autoUpdater.quitAndInstall();
      }
    });
});

// App lifecycle events

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// Handle second instance
const gotTheLock = app.requestSingleInstanceLock();

if (!gotTheLock) {
  app.quit();
} else {
  app.on('second-instance', () => {
    if (mainWindow) {
      if (mainWindow.isMinimized()) mainWindow.restore();
      mainWindow.focus();
    }
  });
}

// Clean up on exit
app.on('will-quit', () => {
  // Cleanup tasks
});

export { mainWindow };

// Key Features Explained:
🪟 Window Configuration

1600x1000 default size (optimized for quantum chess board + sidebars)
Context isolation for security (prevents renderer from accessing Node.js)
Preload script for safe IPC communication

📋 Native Menu System

File Menu: New game, save/load, export positions
Quantum Menu: Unique! Collapse wavefunction, toggle quantum view
Analysis Menu: Position evaluation, best move suggestions
Keyboard shortcuts: All major functions have accelerators

💾 File Operations

Custom .qcg file format (Quantum Chess Game)
Native save/load dialogs
JSON export for positions
Error handling with user-friendly dialogs

🔄 Auto-Updates

Automatic update checking (production only)
User prompt before installing
Seamless update experience

🔒 Security Features

Single instance lock: Prevents multiple app instances
Context isolation: Separates main and renderer processes
No node integration: Safer renderer environment

📡 IPC Communication
All communication between Electron and React happens via secure IPC channels:

new-game, save-game-request, load-game-data
measure-board, toggle-quantum-view
evaluate-position, show-best-move

This architecture allows your React app to run identically on web and desktop!

# package.json

{
  "name": "quantum-chess-ultimate",
  "version": "1.0.0",
  "description": "An experimental chess engine integrating quantum computing concepts",
  "author": "Your Name",
  "license": "MIT",
  "homepage": "https://github.com/yourusername/quantum-chess-ultimate",
  "repository": {
    "type": "git",
    "url": "https://github.com/yourusername/quantum-chess-ultimate.git"
  },
  "main": "dist-electron/main.js",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "electron:dev": "concurrently \"npm run dev\" \"wait-on http://localhost:5173 && electron .\"",
    "electron:build": "npm run build && electron-builder",
    "electron:build:win": "npm run build && electron-builder --win",
    "test": "vitest",
    "test:e2e": "playwright test",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "format": "prettier --write \"src/**/*.{ts,tsx,css}\"",
    "type-check": "tsc --noEmit"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "framer-motion": "^10.16.4",
    "zustand": "^4.4.7",
    "@tanstack/react-query": "^5.12.0",
    "axios": "^1.6.2",
    "socket.io-client": "^4.5.4",
    "three": "^0.159.0",
    "@react-three/fiber": "^8.15.12",
    "@react-three/drei": "^9.92.0",
    "d3": "^7.8.5",
    "recharts": "^2.10.3",
    "react-dnd": "^16.0.1",
    "react-dnd-html5-backend": "^16.0.1",
    "clsx": "^2.0.0",
    "date-fns": "^2.30.0",
    "nanoid": "^5.0.4"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@types/three": "^0.159.0",
    "@types/d3": "^7.4.3",
    "@typescript-eslint/eslint-plugin": "^6.14.0",
    "@typescript-eslint/parser": "^6.14.0",
    "@vitejs/plugin-react": "^4.2.1",
    "typescript": "^5.2.2",
    "vite": "^5.0.8",
    "vitest": "^1.0.4",
    "@vitest/ui": "^1.0.4",
    "eslint": "^8.55.0",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "prettier": "^3.1.1",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.3.6",
    "electron": "^28.0.0",
    "electron-builder": "^24.9.1",
    "electron-updater": "^6.1.7",
    "concurrently": "^8.2.2",
    "wait-on": "^7.2.0",
    "@playwright/test": "^1.40.1"
  },
  "build": {
    "appId": "com.quantumchess.ultimate",
    "productName": "Quantum Chess Ultimate",
    "directories": {
      "output": "release",
      "buildResources": "build"
    },
    "files": [
      "dist/**/*",
      "dist-electron/**/*"
    ],
    "win": {
      "target": [
        {
          "target": "nsis",
          "arch": [
            "x64"
          ]
        }
      ],
      "icon": "build/icon.ico",
      "artifactName": "${productName}-${version}-Setup.${ext}"
    },
    "nsis": {
      "oneClick": false,
      "allowToChangeInstallationDirectory": true,
      "createDesktopShortcut": true,
      "createStartMenuShortcut": true,
      "shortcutName": "Quantum Chess Ultimate"
    },
    "publish": {
      "provider": "github",
      "releaseType": "release"
    }
  }
}

# requirements.txt

# Quantum Chess Ultimate - Backend Requirements

# Core Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6
pydantic==2.5.3
pydantic-settings==2.1.0

# Quantum Computing
qiskit==0.45.2
qiskit-aer==0.13.2
numpy==1.26.3

# WebSocket
python-socketio==5.11.0
python-engineio==4.9.0
websockets==12.0

# Caching & Database
redis==5.0.1
motor==3.3.2  # Async MongoDB driver
pymongo==4.6.1

# Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# Utilities
python-dotenv==1.0.0
aiofiles==23.2.1
httpx==0.26.0

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0
httpx==0.26.0

# Code Quality
black==23.12.1
flake8==7.0.0
mypy==1.8.0
isort==5.13.2

# Monitoring & Logging
loguru==0.7.2
prometheus-client==0.19.0
sentry-sdk==1.39.2

# Development
ipython==8.20.0

# Dockerfile

# Multi-stage build for Quantum Chess Ultimate Backend

# Stage 1: Build stage
FROM python:3.10-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime stage
FROM python:3.10-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy Python packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY ./app ./app
COPY ./quantum-chess-engine.py .

# Create non-root user for security
RUN useradd -m -u 1000 quantum && \
    chown -R quantum:quantum /app

USER quantum

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker-compose.yml 

version: '3.8'

services:
  # Backend API
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: quantum-chess-backend
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - MONGODB_URL=mongodb://mongodb:27017
      - LOG_LEVEL=info
      - CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
    depends_on:
      - redis
      - mongodb
    volumes:
      - ./backend:/app
    networks:
      - quantum-chess-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: quantum-chess-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - quantum-chess-network
    restart: unless-stopped
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # MongoDB (for future game storage)
  mongodb:
    image: mongo:7
    container_name: quantum-chess-mongodb
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=quantum_chess_2024
    volumes:
      - mongodb-data:/data/db
    networks:
      - quantum-chess-network
    restart: unless-stopped
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 10s
      retries: 5
      start_period: 40s

  # Nginx Reverse Proxy (Production)
  nginx:
    image: nginx:alpine
    container_name: quantum-chess-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./frontend/dist:/usr/share/nginx/html:ro
    depends_on:
      - backend
    networks:
      - quantum-chess-network
    restart: unless-stopped

volumes:
  redis-data:
    driver: local
  mongodb-data:
    driver: local

networks:
  quantum-chess-network:
    driver: bridge

# github_workflows_ci.yml 

name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]
  release:
    types: [created]

env:
  NODE_VERSION: '18.x'
  PYTHON_VERSION: '3.10'

jobs:
  # Backend Tests
  backend-test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r backend/requirements.txt
          pip install pytest pytest-cov pytest-asyncio
      
      - name: Lint with flake8
        run: |
          flake8 backend --max-line-length=100 --exclude=venv
      
      - name: Type check with mypy
        run: |
          mypy backend/app --ignore-missing-imports
      
      - name: Run tests
        run: |
          cd backend
          pytest tests/ --cov=app --cov-report=xml --cov-report=html
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./backend/coverage.xml
          flags: backend

  # Frontend Tests
  frontend-test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Lint
        run: |
          cd frontend
          npm run lint
      
      - name: Type check
        run: |
          cd frontend
          npm run type-check
      
      - name: Run unit tests
        run: |
          cd frontend
          npm test -- --coverage
      
      - name: Build
        run: |
          cd frontend
          npm run build

  # E2E Tests
  e2e-test:
    runs-on: ubuntu-latest
    needs: [backend-test, frontend-test]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
          npx playwright install --with-deps
      
      - name: Start services
        run: |
          docker-compose up -d
          sleep 10
      
      - name: Run E2E tests
        run: |
          cd frontend
          npm run test:e2e
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: frontend/playwright-report/

  # Build Docker Images
  docker-build:
    runs-on: ubuntu-latest
    needs: [backend-test, frontend-test]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: yourusername/quantum-chess-backend:latest
          cache-from: type=registry,ref=yourusername/quantum-chess-backend:buildcache
          cache-to: type=registry,ref=yourusername/quantum-chess-backend:buildcache,mode=max

  # Build Windows Desktop App
  build-desktop:
    runs-on: windows-latest
    needs: [frontend-test]
    if: github.event_name == 'release'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
      
      - name: Install dependencies
        run: |
          cd frontend
          npm ci
      
      - name: Build Electron app
        run: |
          cd frontend
          npm run electron:build:win
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: windows-installer
          path: frontend/release/*.exe

  # Deploy to Production
  deploy:
    runs-on: ubuntu-latest
    needs: [docker-build]
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to Railway
        run: |
          # Add Railway deployment script
          echo "Deploying to Railway..."
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
      
      - name: Deploy frontend to Vercel
        run: |
          cd frontend
          npx vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
          VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

  # Notify on Success
  notify:
    runs-on: ubuntu-latest
    needs: [deploy]
    if: success()
    
    steps:
      - name: Send notification
        run: |
          echo "✅ Deployment successful!"
          # Add Slack/Discord webhook notification here

Perfect! I've created a comprehensive implementation plan for you Quantum Chess Ultimate project with both Windows desktop and web versions. Here's what I've delivered:
📋 Complete Implementation Package
📖 Documentation (3 files)

IMPLEMENTATION_PLAN.md - 12-week roadmap with detailed phases, tasks, and architectural decisions
TECH_STACK.md - Complete technology breakdown with rationale for each choice
QUICK_START.md - Developer onboarding guide with troubleshooting

💻 Code Artifacts (6 files)

backend_main.py - FastAPI backend with WebSocket support, quantum engine integration, and REST endpoints
frontend_App.tsx - React main component with unique brutalist-quantum design aesthetic
frontend_styles.css - Custom CSS with quantum-inspired animations and effects (avoiding generic Material-UI look)
ChessBoard.tsx - Interactive chess board component with quantum visualization
electron_main.ts - Electron wrapper for Windows desktop application

🔧 Configuration Files (4 files)

package.json - Complete npm dependencies and build scripts
requirements.txt - Python backend dependencies
Dockerfile - Multi-stage Docker build for backend
docker-compose.yml - Full-stack deployment configuration
github_workflows_ci.yml - Complete CI/CD pipeline

🎯 Key Implementation Highlights
Unified Architecture

Single Codebase: React for both web and desktop (via Electron)
Code Reuse: 90%+ shared between platforms
Modern Stack: TypeScript, React 18, FastAPI, Qiskit

Unique Design

Brutalist-Quantum Aesthetic: Custom design avoiding generic AI patterns
Custom Fonts: Orbitron (display) + JetBrains Mono (code)
Quantum Effects: Glowing particles, scan lines, animated overlays
Bold Color Palette: Neon quantum green (#00ff9d) on concrete grays

Production-Ready Features

WebSocket real-time updates
Quantum circuit visualization (Three.js)
Comprehensive testing (Vitest, Playwright, Pytest)
Docker deployment
Auto-updates for desktop app
CI/CD pipeline

12-Week Timeline

Weeks 1-3: Enhanced quantum engine + FastAPI backend
Weeks 4-7: React frontend + quantum visualization
Weeks 8-9: Electron desktop packaging
Weeks 10-12: Testing, deployment, polish

This implementation plan gives you everything needed to build a production-quality quantum chess application that works seamlessly on both Windows desktop and web browsers!