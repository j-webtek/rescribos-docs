# Cart-Based Workflow

### 6.2 Cart-Based Workflow

The **Cart System** allows users to curate collections of stories for custom reports:

**Implementation (`src/electron/cartManager.js`):**
```javascript
class CartManager {
    constructor() {
        this.cartPath = path.join(app.getPath('userData'),
                                   'storage', 'cart');
        this.carts = new Map();
    }

    createCart(name = 'default') {
        const cart = {
            id: this.generateCartId(),
            name: name,
            created_at: new Date().toISOString(),
            stories: [],
            tags: [],
            notes: ''
        };

        this.carts.set(cart.id, cart);
        this.saveCart(cart);
        return cart;
    }

    addStoryToCart(cartId, story) {
        const cart = this.carts.get(cartId);

        // Prevent duplicates
        if (cart.stories.find(s => s.id === story.id)) {
            return { success: false, reason: 'Already in cart' };
        }

        cart.stories.push(story);
        cart.updated_at = new Date().toISOString();
        this.saveCart(cart);

        return { success: true, cart: cart };
    }

    removeStoryFromCart(cartId, storyId) {
        const cart = this.carts.get(cartId);
        cart.stories = cart.stories.filter(s => s.id !== storyId);
        this.saveCart(cart);
    }

    generateReportFromCart(cartId) {
        const cart = this.carts.get(cartId);

        // Send cart stories to Python for full analysis
        return this.pythonBridge.call('generate_cart_report', {
            stories: cart.stories,
            cart_name: cart.name,
            user_notes: cart.notes
        });
    }
}
```

**Cart Features:**
- **Multiple Carts:** Organize by project, topic, client
- **Drag-and-Drop:** Add stories from search results
- **Manual Notes:** Annotate cart with context
- **Custom Reports:** Generate thematic analysis from cart
- **Export Options:** PDF, DOCX, Markdown
- **Sharing:** Export cart as JSON for collaboration

**Use Cases:**
- Competitive intelligence tracking
- Research paper collection
- Due diligence materials
- Content curation for newsletters
- Client-specific reports
