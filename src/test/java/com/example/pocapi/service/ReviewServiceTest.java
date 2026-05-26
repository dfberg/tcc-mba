package com.example.pocapi.service;

import com.example.pocapi.exception.ResourceNotFoundException;
import com.example.pocapi.exception.ValidationException;
import com.example.pocapi.model.dto.ReviewDTO;
import com.example.pocapi.model.entity.Book;
import com.example.pocapi.model.entity.Review;
import com.example.pocapi.model.entity.Author;
import com.example.pocapi.repository.BookRepository;
import com.example.pocapi.repository.ReviewRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("ReviewService Unit Tests")
class ReviewServiceTest {
    
    @Mock
    private ReviewRepository reviewRepository;
    
    @Mock
    private BookRepository bookRepository;
    
    @InjectMocks
    private ReviewService reviewService;
    
    private Review testReview;
    private Book testBook;
    private Author testAuthor;
    private ReviewDTO testReviewDTO;
    
    @BeforeEach
    void setUp() {
        testAuthor = Author.builder()
                .id(1L)
                .name("Test Author")
                .email("test@example.com")
                .build();
        
        testBook = Book.builder()
                .id(1L)
                .title("Test Book")
                .isbn("123456789")
                .author(testAuthor)
                .build();
        
        testReview = Review.builder()
                .id(1L)
                .rating(5)
                .content("Great book!")
                .book(testBook)
                .build();
        
        testReviewDTO = ReviewDTO.builder()
                .rating(5)
                .content("Great book!")
                .bookId(1L)
                .build();
    }
    
    @Test
    @DisplayName("should create review successfully")
    void testCreateReviewSuccess() {
        // Arrange
        when(bookRepository.findById(1L)).thenReturn(Optional.of(testBook));
        when(reviewRepository.save(any(Review.class))).thenReturn(testReview);
        
        // Act
        ReviewDTO result = reviewService.createReview(testReviewDTO);
        
        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getRating()).isEqualTo(5);
        assertThat(result.getContent()).isEqualTo("Great book!");
        verify(reviewRepository, times(1)).save(any(Review.class));
    }
    
    @Test
    @DisplayName("should throw validation exception when rating is invalid")
    void testCreateReviewWithInvalidRating() {
        // Arrange
        ReviewDTO invalidDTO = ReviewDTO.builder()
                .rating(6)  // Invalid: should be 1-5
                .content("Great book!")
                .bookId(1L)
                .build();
        
        // Act & Assert
        assertThatThrownBy(() -> reviewService.createReview(invalidDTO))
                .isInstanceOf(ValidationException.class)
                .hasMessage("Review rating must be between 1 and 5");
        
        verify(reviewRepository, never()).save(any());
    }
    
    @Test
    @DisplayName("should throw exception when book not found")
    void testCreateReviewWithInvalidBook() {
        // Arrange
        when(bookRepository.findById(999L)).thenReturn(Optional.empty());
        
        ReviewDTO invalidDTO = ReviewDTO.builder()
                .rating(4)
                .content("Great book!")
                .bookId(999L)
                .build();
        
        // Act & Assert
        assertThatThrownBy(() -> reviewService.createReview(invalidDTO))
                .isInstanceOf(ResourceNotFoundException.class);
        
        verify(reviewRepository, never()).save(any());
    }
}
