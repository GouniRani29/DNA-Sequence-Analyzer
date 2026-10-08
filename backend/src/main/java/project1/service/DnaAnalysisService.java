package project1.service;

import java.util.List;
import java.util.Map;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import project1.entity.DnaAnalysis;
import project1.repository.DnaAnalysisRepository;

@Service
public class DnaAnalysisService {

    private final DnaAnalysisRepository repository;
    private final RestTemplate restTemplate;

    private final String FLASK_URL =
            "http://127.0.0.1:5000/predict";

    public DnaAnalysisService(
            DnaAnalysisRepository repository,
            RestTemplate restTemplate) {

        this.repository = repository;
        this.restTemplate = restTemplate;
    }

    // =====================================================
    // ANALYZE DNA
    // =====================================================

    public DnaAnalysis analyzeDNA(String sequence) {

        // -------------------------------------------------
        // 1. Validate input
        // -------------------------------------------------

        if (sequence == null || sequence.trim().isEmpty()) {

            throw new RuntimeException(
                    "DNA sequence cannot be empty"
            );
        }

        // -------------------------------------------------
        // 2. Prepare request for Flask
        // -------------------------------------------------

        Map<String, String> request = Map.of(
                "sequence",
                sequence
        );

        System.out.println(
                "Sending DNA sequence to Flask..."
        );

        // -------------------------------------------------
        // 3. Call Flask Transformer API
        // -------------------------------------------------

        Map<?, ?> response;

        try {

            response = restTemplate.postForObject(
                    FLASK_URL,
                    request,
                    Map.class
            );

        } catch (Exception e) {

            throw new RuntimeException(
                    "Could not connect to ML service: "
                    + e.getMessage()
            );
        }

        // -------------------------------------------------
        // 4. Check response
        // -------------------------------------------------

        if (response == null) {

            throw new RuntimeException(
                    "No response received from ML service"
            );
        }

        System.out.println(
                "Flask Response: " + response
        );

        // -------------------------------------------------
        // 5. Check success
        // -------------------------------------------------

        Boolean success =
                (Boolean) response.get("success");

        if (!Boolean.TRUE.equals(success)) {

            throw new RuntimeException(
                    "ML prediction failed"
            );
        }

        // -------------------------------------------------
        // 6. Get prediction
        // -------------------------------------------------

        Number predictedClass =
                (Number) response.get(
                        "predictedClass"
                );

        Number confidence =
                (Number) response.get(
                        "confidence"
                );

        if (predictedClass == null ||
                confidence == null) {

            throw new RuntimeException(
                    "Invalid response from ML service"
            );
        }

        // -------------------------------------------------
        // 7. Create database entity
        // -------------------------------------------------

        DnaAnalysis analysis =
                new DnaAnalysis();

        analysis.setSequence(
                sequence
        );

        analysis.setPrediction(
                String.valueOf(
                        predictedClass.intValue()
                )
        );

        analysis.setConfidence(
                confidence.doubleValue()
        );

        // -------------------------------------------------
        // 8. Save to MySQL
        // -------------------------------------------------

        DnaAnalysis saved =
                repository.save(analysis);

        System.out.println(
                "DNA analysis saved successfully. ID: "
                + saved.getId()
        );

        return saved;
    }

    // =====================================================
    // GET ALL
    // =====================================================

    public List<DnaAnalysis> getAllAnalyses() {

        return repository.findAll();
    }

    // =====================================================
    // GET BY ID
    // =====================================================

    public DnaAnalysis getAnalysisById(Long id) {

        return repository.findById(id)
                .orElseThrow(() ->
                        new RuntimeException(
                                "Analysis not found"
                        )
                );
    }
 // =====================================================
 // UPDATE DNA ANALYSIS
 // =====================================================

 public DnaAnalysis updateAnalysis(
         Long id,
         String sequence,
         String prediction,
         Double confidence) {

     DnaAnalysis analysis = repository.findById(id)
             .orElseThrow(() ->
                     new RuntimeException("Analysis not found")
             );

     analysis.setSequence(sequence);
     analysis.setPrediction(prediction);
     analysis.setConfidence(confidence);

     return repository.save(analysis);
 }
    // =====================================================
    // DELETE
    // =====================================================

    public void deleteAnalysis(Long id) {

        if (!repository.existsById(id)) {

            throw new RuntimeException(
                    "Analysis not found"
            );
        }

        repository.deleteById(id);
    }
}