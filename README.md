# ke

## Class-Attribute Schema Pattern:

The ontology defines classes like `Song`, `Album`, `Artist`, `Bridge`, `Outro`, and `Verse`, and associates attributes to instances of these classes using properties like `core:title`, `core:name`, `mm:hasAnnotation`, `mm:hasText`, and `ex:fragmentName`.  
For example, the `Album` class has a `core:title` attribute, the `Artist` class has a `core:name` attribute, and the `Verse` class has `mm:hasText` and `mm:hasAnnotation` attributes.

## Part-Whole Schema Pattern:

The ontology employs a part-whole relationship: any object in a collection is a part of the whole composition and composition as a whole is a collection of parts, where a `Song` is divided into parts like `Bridge`, `Outro`, and `Verse`, represented by the `core:hasPart` property.  
For instance, the song "Yesterday" has parts like `Bridge`, `Outro`, and `Verse`, as seen in the triples with the `core:hasPart` predicate.

## Participation Schema Pattern:

The ontology also depicts participation relationships where a `Song` is associated with an `Artist` and an `Album` through the properties `mm:isInvolvedIn` and `mm:isPartOfRelease` respectively.  
For instance, the song "Yesterday" is associated with the artist "The Beatles" and the album "Help!" through the `mm:isInvolvedIn` and `mm:isPartOfRelease` properties respectively.
