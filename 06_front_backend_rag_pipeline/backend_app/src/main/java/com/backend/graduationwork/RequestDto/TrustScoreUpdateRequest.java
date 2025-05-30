package com.backend.graduationwork.RequestDto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class TrustScoreUpdateRequest {
    private double reviewLength;
    private double reviewCount;
    private double sentiment;
    private double photo;
    private double recentness;
    private double threshold;
}
