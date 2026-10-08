package project1.controller;

import java.util.List;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import project1.entity.DnaAnalysis;
import project1.service.DnaAnalysisService;

@RestController
@RequestMapping("/analysis")
@CrossOrigin(origins = "*")
public class DnaAnalysisController {

    private final DnaAnalysisService dnaAnalysisService;

    public DnaAnalysisController(DnaAnalysisService dnaAnalysisService) {
        this.dnaAnalysisService = dnaAnalysisService;
    }

    // =====================================================
    // CREATE / ANALYZE DNA
    // =====================================================

    @PostMapping
    public ResponseEntity<DnaAnalysis> analyzeDNA(
            @RequestBody DnaAnalysis request) {

        DnaAnalysis result =
                dnaAnalysisService.analyzeDNA(
                        request.getSequence()
                );

        return ResponseEntity.ok(result);
    }

    // =====================================================
    // GET ALL ANALYSES
    // =====================================================

    @GetMapping
    public ResponseEntity<List<DnaAnalysis>> getAllAnalyses() {

        return ResponseEntity.ok(
                dnaAnalysisService.getAllAnalyses()
        );
    }

    // =====================================================
    // GET ANALYSIS BY ID
    // =====================================================

    @GetMapping("/{id}")
    public ResponseEntity<DnaAnalysis> getAnalysisById(
            @PathVariable Long id) {

        return ResponseEntity.ok(
                dnaAnalysisService.getAnalysisById(id)
        );
    }

    // =====================================================
    // DELETE ANALYSIS
    // =====================================================

    @DeleteMapping("/{id}")
    public ResponseEntity<String> deleteAnalysis(
            @PathVariable Long id) {

        dnaAnalysisService.deleteAnalysis(id);

        return ResponseEntity.ok(
                "Analysis deleted successfully"
        );
    }
}