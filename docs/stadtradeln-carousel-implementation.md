# Stadtradeln Carousel Implementation Documentation

**Created**: June 23, 2026  
**Purpose**: Document the carousel implementation for the Stadtradeln Aktionstag flyer and provide reversion instructions

## Overview

This document describes the implementation of a carousel-based display for Stadtradeln widgets and the event flyer, replacing the original two-column grid layout.

## Original State (Before Carousel)

### Original Layout Description

The homepage originally displayed two Stadtradeln widgets side-by-side in a responsive grid:
- **Left column**: Team Rankings Widget
- **Right column**: Municipality Rankings Widget
- **Mobile behavior**: Widgets stack vertically

### Original File: `see_more.html`

**Location**: `/layouts/partials/see_more.html`

**Original Content**:
```html
{{/* STADTRADELN Statistics Section */}}
{{ if isset .Site.Params "stadtradeln" }}
{{ if .Site.Params.stadtradeln.enable }}
<section class="bar background-image-fixed-2 no-mb color-white text-center" style="padding: 30px 0;">
    <div class="dark-mask"></div>
    <div class="container stadtradeln-widgets-container">
        <div class="row">
            <div class="col-md-6 col-sm-12">
                {{ partial "stadtradeln-teams.html" . }}
            </div>
            <div class="col-md-6 col-sm-12">
                {{ partial "stadtradeln-municipalities.html" . }}
            </div>
        </div>
    </div>
<script src="/js/stadtradeln-autoscroll.js"></script>
</section>
{{ end }}
{{ end }}
```

### Original Configuration

**File**: `config.toml` (lines 158-165)

```toml
### STADTRADELN Live Statistics
[params.stadtradeln]
    enable = true
    teams_title = "Team-Rankings im Rhein-Neckar-Kreis"
    municipalities_title = "Gemeinde-Rankings im Rhein-Neckar-Kreis"
    highlight_team = "Équipe Vélo Village Eschelbronn"
    highlight_municipality = "Eschelbronn"
    top_n = 20
```

## Carousel Implementation

### Event Context

**Event**: Stadtradeln Aktionstag "Radmarathon für Jedermann"  
**Date**: June 28, 2026  
**Flyer**: `/content/posts/2026/AmtsblattKW26_2/Stadtradeln-Aktionstag_Flyer.png`  
**Blog Post**: `/content/posts/2026/AmtsblattKW26_2/index.md`

### Implementation Rationale

The carousel was implemented to:
1. Prominently display the event flyer alongside existing statistics widgets
2. Create a more dynamic, attention-grabbing presentation
3. Use screen space efficiently while showing three pieces of content
4. Leverage existing Owl Carousel infrastructure in the theme

### Files Created/Modified

#### New Files
1. `/layouts/partials/stadtradeln-carousel.html` - Carousel HTML structure
2. `/static/css/stadtradeln-carousel.css` - Carousel styling
3. `/docs/stadtradeln-carousel-implementation.md` - This documentation

#### Modified Files
1. `/layouts/partials/see_more.html` - Replaced grid with carousel
2. `/themes/hugo-universal-theme/static/js/front.js` - Added carousel initialization
3. `/themes/hugo-universal-theme/layouts/partials/head.html` - Added CSS reference
4. `config.toml` - Added carousel configuration (optional)

### Features

- **Three Slides**: Team rankings, municipality rankings, event flyer
- **Auto-rotation**: 5-second intervals with pause on hover
- **Manual Navigation**: Prev/next arrows and pagination dots
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Maintained Functionality**: All existing widget features preserved

## Reversion Instructions

When the event has passed and the flyer is no longer relevant:

### Quick Reversion (Recommended)

If configuration-based toggle was implemented:

**File**: `config.toml`

Change:
```toml
[params.stadtradeln.carousel]
    enable = false
```

### Manual Reversion

Restore the original two-column grid layout:

**File**: `/layouts/partials/see_more.html`

Replace the carousel container with the original grid:

```html
<div class="container stadtradeln-widgets-container">
    <div class="row">
        <div class="col-md-6 col-sm-12">
            {{ partial "stadtradeln-teams.html" . }}
        </div>
        <div class="col-md-6 col-sm-12">
            {{ partial "stadtradeln-municipalities.html" . }}
        </div>
    </div>
</div>
```

Use the original code shown in the "Original File" section above.

### Complete Removal

To fully remove carousel functionality:

1. **Delete new files**:
   ```bash
   rm /layouts/partials/stadtradeln-carousel.html
   rm /static/css/stadtradeln-carousel.css
   ```

2. **Restore `see_more.html`**: Use the original content shown above

3. **Remove carousel initialization**:
   - **File**: `/themes/hugo-universal-theme/static/js/front.js`
   - Remove the STADTRADELN carousel initialization block

4. **Remove CSS reference**:
   - **File**: `/themes/hugo-universal-theme/layouts/partials/head.html`
   - Remove: `<link href="{{ "css/stadtradeln-carousel.css" | relURL }}" rel="stylesheet">`

5. **Clean configuration**:
   - **File**: `config.toml`
   - Remove `[params.stadtradeln.carousel]` section

## Testing After Reversion

After reverting to the grid layout:

1. Run `hugo server`
2. Navigate to homepage: `http://localhost:1313/de/`
3. Verify two widgets display side-by-side
4. Verify widgets still show highlighted entries
5. Verify auto-scroll functionality still works
6. Test mobile responsive behavior (widgets stack vertically)
7. Check browser console for any errors

## Contact

For questions or issues with this implementation:
- Check Hugo build logs for errors
- Review this documentation for reversion steps
- Refer to the original plan file in `.claude/plans/`

## Version History

- **v1.0 (June 23, 2026)**: Initial carousel implementation for Stadtradeln Aktionstag
- **Pre-carousel**: Two-column grid layout (documented above)
