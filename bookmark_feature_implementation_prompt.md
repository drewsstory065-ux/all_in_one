# AI Implementation Prompt: Bookmark Feature for MyBrowser

## Project Context and Architecture

### Application Overview
- **Project**: MyBrowser - PyQt6-based web browser
- **Current Features**: Multi-tab browsing, navigation, history system
- **Architecture**: Modular design with single-responsibility classes
- **Technology Stack**: Python 3, PyQt6, QtWebEngine

### Current Code Structure
```
app/mybrowser/
├── mybrowser_window.py     # Main window orchestrator
├── navigation_bar.py       # Navigation controls
├── tab_widget.py          # Tab management
├── web_view.py            # Web engine wrapper
├── history_model.py       # History data management
└── history_widget.py      # History UI component
```

### Key Architectural Principles
1. **Single Responsibility**: Each class has one focused purpose
2. **Maximum 150 Lines**: All class implementations under 150 lines
3. **Signal-Based Communication**: Use Qt signals for loose coupling
4. **Persistent Storage**: JSON-based storage for user data
5. **Modular Design**: Independent, reusable components

## Bookmark Feature Requirements

### Core Functionality
1. **Bookmark Storage**: Persistent storage of bookmarked URLs with titles
2. **Bookmark UI**: Button in navigation bar to toggle bookmark menu
3. **Bookmark Management**: Add/remove bookmarks, organize by folders
4. **Quick Access**: Click bookmarks to open in current or new tab

### User Interface Components
- **Bookmark Button**: "B" button in navigation bar (similar to history "H" button)
- **Bookmark Menu**: Popup dialog showing bookmarked pages
- **Add Bookmark**: Button to bookmark current page
- **Bookmark Folders**: Optional organization system
- **Context Menu**: Right-click options for bookmark management

### Technical Specifications
- **Storage Format**: JSON file in application data directory
- **Maximum Bookmarks**: Configurable limit (default: 200)
- **Data Structure**: URL, title, timestamp, folder/category
- **UI Integration**: Seamless integration with existing navigation bar

## Implementation Guidelines

### 1. File Structure
Create these new files:
- `app/mybrowser/bookmark_model.py` - Bookmark data management
- `app/mybrowser/bookmark_widget.py` - Bookmark UI component

### 2. Bookmark Model (bookmark_model.py)
```python
# Follow history_model.py pattern but for bookmarks
class BookmarkItem:
    # URL, title, timestamp, folder
    pass

class BookmarkModel(QObject):
    # CRUD operations, persistent storage
    # Signals: bookmark_added, bookmark_removed, bookmarks_changed
    pass
```

### 3. Bookmark Widget (bookmark_widget.py)
```python
# Follow history_widget.py pattern
class BookmarkWidget(QWidget):
    # List of bookmarks with context menu
    # Add/remove bookmark buttons
    # Folder organization (optional)
    pass
```

### 4. Navigation Bar Integration
- Add "B" button next to history button
- Connect to bookmark toggle functionality
- Update navigation_bar.py following existing pattern

### 5. Main Window Integration
- Initialize bookmark components in mybrowser_window.py
- Connect signals for bookmark management
- Handle bookmark actions (open in tab, etc.)

## Lessons Learned from Previous Implementation

### Success Patterns to Replicate
1. **Signal Handling**: Use proper signal disconnection with try/except blocks
2. **Persistent Storage**: Follow JSON storage pattern from history_model.py
3. **UI Positioning**: Position popup widgets relative to navigation bar
4. **Error Handling**: Graceful handling of missing connections and file operations

### Common Mistakes to Avoid
1. **Signal Disconnect Errors**: Always use try/except when disconnecting signals
2. **Initial Tab Connection**: Ensure initial tab connects to all tracking systems
3. **Widget Visibility**: Set proper window flags for popup dialogs
4. **URL Validation**: Handle edge cases like "about:blank" and data URLs

### Proven Approaches
1. **Model-View Separation**: Keep data management separate from UI
2. **Event-Driven Architecture**: Use signals for component communication
3. **Progressive Enhancement**: Start with basic features, add complexity later
4. **Consistent Naming**: Follow existing naming conventions and patterns

## Development Workflow

### Step 1: Data Model
- Implement BookmarkItem and BookmarkModel classes
- Test persistent storage functionality
- Ensure proper signal emission

### Step 2: UI Components
- Create BookmarkWidget with list and buttons
- Implement context menu for bookmark actions
- Test UI interactions independently

### Step 3: Integration
- Add bookmark button to navigation bar
- Connect bookmark model to main window
- Test end-to-end functionality

### Step 4: Enhancement
- Add folder organization (optional)
- Implement drag-and-drop reordering
- Add bookmark import/export features

## Testing Checklist
- [ ] Bookmark persistence across browser sessions
- [ ] Add/remove bookmark functionality
- [ ] Bookmark menu opens/closes properly
- [ ] Clicking bookmarks opens correct URLs
- [ ] Navigation bar integration works
- [ ] Error handling for invalid URLs
- [ ] Performance with large bookmark collections

## Git Best Practices
- **Commit Messages**: Use conventional commit format
- **Branch Strategy**: Feature branches for new functionality
- **Code Review**: Self-review against architectural principles
- **Documentation**: Update README with new features

## MCP Server Usage
- Use Git MCP server for version control operations
- Follow established commit message patterns
- Push changes to main branch after testing

## Expected Challenges and Solutions
1. **Signal Management**: Use the proven try/except pattern for disconnects
2. **UI Positioning**: Follow history widget positioning approach
3. **Data Consistency**: Implement proper error handling for file operations
4. **Performance**: Use efficient data structures for bookmark search

## Success Metrics
- All classes under 150 lines
- No runtime errors in console
- Persistent storage working correctly
- Seamless integration with existing features
- User-friendly bookmark management

This prompt provides a comprehensive roadmap based on proven implementation patterns from the successful multi-tab and history features. The AI should follow this structured approach to ensure consistent, maintainable code that integrates seamlessly with the existing architecture.
